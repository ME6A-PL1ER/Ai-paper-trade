import unittest
from src.models.neural_network import NeuralNetwork
from src.models.trading_agent import TradingAgent

class TestNeuralNetwork(unittest.TestCase):
    def setUp(self):
        self.model = NeuralNetwork(input_size=10, hidden_size=5, output_size=3)

    def test_forward_pass(self):
        input_data = [0.1] * 10
        output = self.model.forward(input_data)
        self.assertEqual(len(output), 3)

    def test_training(self):
        input_data = [0.1] * 10
        target = [0, 1, 0]
        loss = self.model.train(input_data, target)
        self.assertIsInstance(loss, float)

class TestTradingAgent(unittest.TestCase):
    def setUp(self):
        self.agent = TradingAgent(model=NeuralNetwork(input_size=10, hidden_size=5, output_size=3))

    def test_decision_making(self):
        market_data = [0.1] * 10
        decision = self.agent.make_decision(market_data)
        self.assertIn(decision, ['buy', 'sell', 'hold'])

if __name__ == '__main__':
    unittest.main()