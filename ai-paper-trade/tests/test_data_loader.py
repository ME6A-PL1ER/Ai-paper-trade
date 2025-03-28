import unittest
from src.data.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.data_loader = DataLoader()

    def test_load_data(self):
        symbol = 'AAPL'
        data = self.data_loader.load_data(symbol)
        self.assertIsNotNone(data)
        self.assertIn('Open', data.columns)
        self.assertIn('Close', data.columns)

    def test_preprocess_data(self):
        symbol = 'AAPL'
        raw_data = self.data_loader.load_data(symbol)
        processed_data = self.data_loader.preprocess_data(raw_data)
        self.assertEqual(processed_data.shape[0], raw_data.shape[0])
        self.assertIn('Normalized_Close', processed_data.columns)

    def test_invalid_symbol(self):
        with self.assertRaises(ValueError):
            self.data_loader.load_data('INVALID_SYMBOL')

if __name__ == '__main__':
    unittest.main()