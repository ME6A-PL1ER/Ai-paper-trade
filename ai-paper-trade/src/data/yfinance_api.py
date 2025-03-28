# yfinance_api.py

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import logging
from functools import lru_cache

class YFinanceAPI:
    def __init__(self, cache_timeout=3600):
        """
        Initialize the YFinance API wrapper.
        
        Parameters:
        cache_timeout (int): Cache timeout in seconds for API calls (default: 1 hour)
        """
        self.logger = logging.getLogger(__name__)
        self.cache_timeout = cache_timeout
        
    def fetch_data(self, symbol, start_date, end_date, interval='1d', actions=True):
        """
        Fetch historical stock data for a given symbol between start_date and end_date.
        
        Parameters:
        symbol (str): The stock symbol to fetch data for.
        start_date (str): The start date for fetching data in 'YYYY-MM-DD' format.
        end_date (str): The end date for fetching data in 'YYYY-MM-DD' format.
        interval (str): Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        actions (bool): Include dividends and stock splits
        
        Returns:
        pandas.DataFrame: A DataFrame containing the historical stock data.
        """
        try:
            data = yf.download(symbol, start=start_date, end=end_date, interval=interval, actions=actions)
            if data.empty:
                self.logger.warning(f"No data found for {symbol} from {start_date} to {end_date}")
            return data
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def fetch_current_price(self, symbol):
        """
        Fetch the current price of a given stock symbol.
        
        Parameters:
        symbol (str): The stock symbol to fetch the current price for.
        
        Returns:
        float: The current price of the stock.
        """
        try:
            stock = yf.Ticker(symbol)
            current_price = stock.history(period='1d')['Close'].iloc[-1]
            return current_price
        except Exception as e:
            self.logger.error(f"Error fetching current price for {symbol}: {str(e)}")
            return None
    
    def fetch_multiple_symbols(self, symbols, start_date=None, end_date=None, interval='1d'):
        """
        Fetch data for multiple symbols at once.
        
        Parameters:
        symbols (list): List of stock symbols to fetch data for.
        start_date (str): The start date for fetching data in 'YYYY-MM-DD' format.
        end_date (str): The end date for fetching data in 'YYYY-MM-DD' format.
        interval (str): Data interval.
        
        Returns:
        dict: A dictionary with symbols as keys and DataFrames as values.
        """
        result = {}
        for symbol in symbols:
            result[symbol] = self.fetch_data(symbol, start_date, end_date, interval)
        return result
    
    @lru_cache(maxsize=128)
    def get_company_info(self, symbol):
        """
        Get company information for a given symbol.
        
        Parameters:
        symbol (str): The stock symbol.
        
        Returns:
        dict: Company information.
        """
        try:
            stock = yf.Ticker(symbol)
            return stock.info
        except Exception as e:
            self.logger.error(f"Error fetching company info for {symbol}: {str(e)}")
            return {}
    
    def get_financials(self, symbol, statement_type='income', period='annual'):
        """
        Get financial statements for a company.
        
        Parameters:
        symbol (str): The stock symbol.
        statement_type (str): Type of statement ('income', 'balance', 'cash').
        period (str): Period ('annual' or 'quarterly').
        
        Returns:
        pandas.DataFrame: Financial statement data.
        """
        try:
            stock = yf.Ticker(symbol)
            if statement_type == 'income':
                return stock.income_stmt if period == 'annual' else stock.quarterly_income_stmt
            elif statement_type == 'balance':
                return stock.balance_sheet if period == 'annual' else stock.quarterly_balance_sheet
            elif statement_type == 'cash':
                return stock.cashflow if period == 'annual' else stock.quarterly_cashflow
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error fetching financials for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def get_options_chain(self, symbol, date=None):
        """
        Get options chain for a specific expiration date.
        
        Parameters:
        symbol (str): The stock symbol.
        date (str): Options expiration date in 'YYYY-MM-DD' format. If None, returns nearest date.
        
        Returns:
        tuple: (calls DataFrame, puts DataFrame)
        """
        try:
            stock = yf.Ticker(symbol)
            dates = stock.options
            
            if not dates:
                return None, None
                
            if date is None:
                date = dates[0]
            elif date not in dates:
                closest_date = min(dates, key=lambda d: abs((datetime.strptime(d, '%Y-%m-%d') - datetime.strptime(date, '%Y-%m-%d')).days))
                date = closest_date
                
            return stock.option_chain(date)
        except Exception as e:
            self.logger.error(f"Error fetching options chain for {symbol}: {str(e)}")
            return None, None
    
    def get_historical_dividends(self, symbol, start_date=None, end_date=None):
        """
        Get historical dividends for a symbol.
        
        Parameters:
        symbol (str): The stock symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        
        Returns:
        pandas.Series: Dividend history.
        """
        try:
            stock = yf.Ticker(symbol)
            return stock.dividends
        except Exception as e:
            self.logger.error(f"Error fetching dividends for {symbol}: {str(e)}")
            return pd.Series()
    
    def get_analyst_recommendations(self, symbol):
        """
        Get analyst recommendations for a stock.
        
        Parameters:
        symbol (str): The stock symbol.
        
        Returns:
        pandas.DataFrame: Analyst recommendations.
        """
        try:
            stock = yf.Ticker(symbol)
            return stock.recommendations
        except Exception as e:
            self.logger.error(f"Error fetching recommendations for {symbol}: {str(e)}")
            return pd.DataFrame()

    def get_major_holders(self, symbol):
        """
        Get major holders of a stock.
        
        Parameters:
        symbol (str): The stock symbol.
        
        Returns:
        tuple: (Major holders DataFrame, Institutional holders DataFrame)
        """
        try:
            stock = yf.Ticker(symbol)
            return stock.major_holders, stock.institutional_holders
        except Exception as e:
            self.logger.error(f"Error fetching major holders for {symbol}: {str(e)}")
            return pd.DataFrame(), pd.DataFrame()
            
    def get_news(self, symbol, limit=10):
        """
        Get recent news for a symbol.
        
        Parameters:
        symbol (str): The stock symbol.
        limit (int): Maximum number of news items to retrieve.
        
        Returns:
        list: List of news items.
        """
        try:
            stock = yf.Ticker(symbol)
            news = stock.news
            return news[:limit] if news and len(news) > limit else news
        except Exception as e:
            self.logger.error(f"Error fetching news for {symbol}: {str(e)}")
            return []
            
    def calculate_technical_indicator(self, data, indicator_type, **kwargs):
        """
        Calculate technical indicators from price data.
        
        Parameters:
        data (pandas.DataFrame): Price data with OHLC columns.
        indicator_type (str): Indicator type ('sma', 'ema', 'rsi', 'macd', 'bollinger').
        **kwargs: Additional parameters for indicators.
        
        Returns:
        pandas.DataFrame or pandas.Series: Calculated indicator.
        """
        try:
            if indicator_type.lower() == 'sma':
                period = kwargs.get('period', 20)
                return data['Close'].rolling(window=period).mean()
            
            elif indicator_type.lower() == 'ema':
                period = kwargs.get('period', 20)
                return data['Close'].ewm(span=period, adjust=False).mean()
            
            elif indicator_type.lower() == 'rsi':
                period = kwargs.get('period', 14)
                delta = data['Close'].diff()
                gain = delta.where(delta > 0, 0).rolling(window=period).mean()
                loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
                rs = gain / loss
                return 100 - (100 / (1 + rs))
            
            elif indicator_type.lower() == 'macd':
                fast = kwargs.get('fast', 12)
                slow = kwargs.get('slow', 26)
                signal = kwargs.get('signal', 9)
                
                fast_ema = data['Close'].ewm(span=fast, adjust=False).mean()
                slow_ema = data['Close'].ewm(span=slow, adjust=False).mean()
                macd_line = fast_ema - slow_ema
                signal_line = macd_line.ewm(span=signal, adjust=False).mean()
                histogram = macd_line - signal_line
                
                result = pd.DataFrame()
                result['macd'] = macd_line
                result['signal'] = signal_line
                result['histogram'] = histogram
                return result
                
            elif indicator_type.lower() == 'bollinger':
                period = kwargs.get('period', 20)
                std_dev = kwargs.get('std_dev', 2)
                
                sma = data['Close'].rolling(window=period).mean()
                std = data['Close'].rolling(window=period).std()
                upper = sma + (std * std_dev)
                lower = sma - (std * std_dev)
                
                result = pd.DataFrame()
                result['middle'] = sma
                result['upper'] = upper
                result['lower'] = lower
                return result
                
            else:
                self.logger.warning(f"Unsupported indicator type: {indicator_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error calculating {indicator_type}: {str(e)}")
            return None
    
    def search_symbols(self, query):
        """
        Search for stock symbols based on company name or ticker.
        
        Parameters:
        query (str): Search query (company name or partial ticker).
        
        Returns:
        list: List of matching symbols and names.
        """
        # Note: yfinance doesn't have a direct search function
        # This is a placeholder - in a real app you might use a separate API or database
        pass
    
    def get_market_status(self):
        """
        Check if the market is currently open.
        
        Returns:
        dict: Market status information.
        """
        # Note: yfinance doesn't provide market status
        # This is a placeholder - in a real app you might use a specialized market API
        pass
    
    def get_sector_performance(self):
        """
        Get sector performance information.
        
        Returns:
        pandas.DataFrame: Sector performance data.
        """
        # This would require parsing sector ETFs or using a specialized API
        pass

    def get_historical_data_with_indicators(self, symbol, start_date, end_date, indicators=None):
        """
        Get historical data with calculated technical indicators.
        
        Parameters:
        symbol (str): The stock symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        indicators (dict): Dictionary of indicators and their parameters.
        
        Returns:
        pandas.DataFrame: Price data with indicators.
        """
        price_data = self.fetch_data(symbol, start_date, end_date)
        if price_data.empty:
            return price_data
            
        if not indicators:
            return price_data
            
        result = price_data.copy()
        
        for indicator, params in indicators.items():
            indicator_data = self.calculate_technical_indicator(price_data, indicator, **params)
            if indicator_data is not None:
                if isinstance(indicator_data, pd.DataFrame):
                    for col in indicator_data.columns:
                        result[f"{indicator}_{col}"] = indicator_data[col]
                else:
                    result[indicator] = indicator_data
                    
        return result