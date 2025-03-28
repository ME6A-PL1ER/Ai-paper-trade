import pandas as pd
from datetime import datetime

class BrokerInterface:
    def __init__(self, api_key=None, api_secret=None, initial_balance=10000, paper_trading=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.paper_trading = paper_trading
        self.balance = initial_balance
        self.positions = {}  # Symbol -> {quantity, avg_price}
        self.transaction_history = []
        self.current_prices = {}  # Cache for current prices
        
        # For paper trading, we don't need real API connections
        if not paper_trading and (api_key is None or api_secret is None):
            raise ValueError("API key and secret are required for live trading")

    def place_order(self, symbol, quantity, order_type='market', price=None):
        """
        Place an order with the brokerage.
        
        :param symbol: The stock symbol to trade.
        :param quantity: The number of shares to buy (positive) or sell (negative).
        :param order_type: The type of order ('market', 'limit', etc.).
        :param price: The price for limit orders (optional).
        :return: Order confirmation or error message.
        """
        if self.paper_trading:
            return self._execute_paper_trade(symbol, quantity, order_type, price)
        else:
            # Implement actual brokerage API call here
            pass
    
    def _execute_paper_trade(self, symbol, quantity, order_type, price=None):
        """Handle paper trading logic"""
        # Get the current price if not provided (for market orders)
        if price is None:
            price = self._get_current_price(symbol)
        
        # Calculate the total cost/proceeds
        total_value = quantity * price
        commission = 0  # No commission for paper trading
        
        # Check if we have enough balance for buying
        if quantity > 0:  # Buy order
            if total_value + commission > self.balance:
                return {
                    "status": "error", 
                    "message": f"Insufficient funds. Required: ${total_value + commission}, Available: ${self.balance}"
                }
            
            # Update balance
            self.balance -= (total_value + commission)
            
            # Update position
            if symbol in self.positions:
                # Calculate new average price
                current_position = self.positions[symbol]
                new_total_quantity = current_position['quantity'] + quantity
                new_total_value = (current_position['quantity'] * current_position['avg_price']) + total_value
                new_avg_price = new_total_value / new_total_quantity
                
                self.positions[symbol] = {
                    'quantity': new_total_quantity,
                    'avg_price': new_avg_price
                }
            else:
                self.positions[symbol] = {
                    'quantity': quantity,
                    'avg_price': price
                }
            
        elif quantity < 0:  # Sell order
            # Check if we have enough shares to sell
            sell_quantity = abs(quantity)
            if symbol not in self.positions or self.positions[symbol]['quantity'] < sell_quantity:
                return {
                    "status": "error", 
                    "message": f"Insufficient shares. Required: {sell_quantity}, Available: {self.positions.get(symbol, {}).get('quantity', 0)}"
                }
            
            # Update balance
            self.balance += (total_value - commission)
            
            # Update position
            current_position = self.positions[symbol]
            new_quantity = current_position['quantity'] - sell_quantity
            
            if new_quantity == 0:
                del self.positions[symbol]  # Remove the position if all shares are sold
            else:
                self.positions[symbol]['quantity'] = new_quantity
        
        # Record the transaction
        self.transaction_history.append({
            'timestamp': datetime.now(),
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'order_type': order_type,
            'total_value': total_value,
            'commission': commission
        })
        
        return {
            "status": "success",
            "message": f"Order executed: {'Bought' if quantity > 0 else 'Sold'} {abs(quantity)} shares of {symbol} at ${price}",
            "order_id": len(self.transaction_history)
        }
    
    def _get_current_price(self, symbol):
        """Get the current price for a symbol (simulated for paper trading)"""
        if symbol in self.current_prices:
            return self.current_prices[symbol]
        
        # In a real implementation, you would fetch from your yfinance_api.py
        # For now, we'll use a placeholder
        try:
            import yfinance as yf
            data = yf.Ticker(symbol).history(period='1d')
            price = float(data['Close'].iloc[-1])
            self.current_prices[symbol] = price
            return price
        except:
            # Default price if fetching fails
            return 100.0  # Placeholder

    def get_account_balance(self):
        """
        Retrieve the current account balance.
        
        :return: Account balance.
        """
        if self.paper_trading:
            return {
                'cash_balance': self.balance,
                'portfolio_value': self.get_portfolio_value(),
                'total_value': self.balance + self.get_portfolio_value()
            }
        else:
            # Implement actual brokerage API call here
            pass

    def get_portfolio_value(self):
        """Calculate the current value of all positions"""
        total_value = 0
        for symbol, position in self.positions.items():
            current_price = self._get_current_price(symbol)
            total_value += position['quantity'] * current_price
        return total_value

    def get_open_positions(self):
        """
        Retrieve a list of open positions in the account.
        
        :return: List of open positions.
        """
        if self.paper_trading:
            result = []
            for symbol, position in self.positions.items():
                current_price = self._get_current_price(symbol)
                market_value = position['quantity'] * current_price
                unrealized_pl = market_value - (position['quantity'] * position['avg_price'])
                
                result.append({
                    'symbol': symbol,
                    'quantity': position['quantity'],
                    'avg_price': position['avg_price'],
                    'current_price': current_price,
                    'market_value': market_value,
                    'unrealized_pl': unrealized_pl,
                    'unrealized_pl_percent': (unrealized_pl / (position['quantity'] * position['avg_price'])) * 100
                })
            return result
        else:
            # Implement actual brokerage API call here
            pass

    def close_position(self, symbol):
        """
        Close an open position for a given stock symbol.
        
        :param symbol: The stock symbol to close.
        :return: Confirmation of position closure.
        """
        if symbol in self.positions:
            quantity = self.positions[symbol]['quantity']
            return self.place_order(symbol, -quantity)  # Negative quantity for selling
        else:
            return {"status": "error", "message": f"No position found for {symbol}"}

    def reset_paper_account(self, initial_balance=10000):
        """Reset the paper trading account to initial state"""
        if self.paper_trading:
            self.balance = initial_balance
            self.positions = {}
            self.transaction_history = []
            return {"status": "success", "message": "Paper trading account has been reset"}
        else:
            return {"status": "error", "message": "Cannot reset a live trading account"}

    def get_transaction_history(self):
        """Get the history of all transactions"""
        return pd.DataFrame(self.transaction_history)

    def update_current_price(self, symbol, price):
        """Update the current price of a symbol (useful for simulation)"""
        self.current_prices[symbol] = price