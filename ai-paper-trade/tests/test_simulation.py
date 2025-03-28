import unittest
from src.simulation.market_simulator import MarketSimulator
from src.simulation.paper_trader import PaperTrader

class TestMarketSimulator(unittest.TestCase):
    def setUp(self):
        self.market_simulator = MarketSimulator()
    
    def test_generate_synthetic_data(self):
        data = self.market_simulator.generate_synthetic_data()
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)

class TestPaperTrader(unittest.TestCase):
    def setUp(self):
        self.paper_trader = PaperTrader()
    
    def test_execute_trade(self):
        initial_balance = self.paper_trader.balance
        self.paper_trader.execute_trade('buy', 10)  # Example trade
        self.assertGreater(self.paper_trader.balance, initial_balance)

    def test_trade_history(self):
        self.paper_trader.execute_trade('buy', 10)
        self.assertEqual(len(self.paper_trader.trade_history), 1)

if __name__ == '__main__':
    unittest.main()