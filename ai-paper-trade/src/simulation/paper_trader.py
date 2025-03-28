class PaperTrader:
    def __init__(self, trading_agent, initial_balance=10000):
        self.trading_agent = trading_agent
        self.balance = initial_balance
        self.position = 0  # Number of shares held
        self.trade_history = []

    def execute_trade(self, action, price):
        if action == 'buy':
            self.position += 1
            self.balance -= price
            self.trade_history.append(('buy', price))
        elif action == 'sell' and self.position > 0:
            self.position -= 1
            self.balance += price
            self.trade_history.append(('sell', price))

    def simulate_trading(self, market_data):
        for data_point in market_data:
            price = data_point['close']
            action = self.trading_agent.predict_action(data_point)
            self.execute_trade(action, price)

    def get_balance(self):
        return self.balance + (self.position * market_data[-1]['close'])

    def get_trade_history(self):
        return self.trade_history

    def reset(self):
        self.balance = 10000
        self.position = 0
        self.trade_history = []