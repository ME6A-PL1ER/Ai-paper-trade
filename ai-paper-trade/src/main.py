# ai-paper-trade/src/main.py

import yfinance as yf
from data.data_loader import DataLoader
from models.neural_network import NeuralNetwork
from models.trading_agent import TradingAgent
from simulation.market_simulator import MarketSimulator
from simulation.paper_trader import PaperTrader
from training.reinforcement_learning import ReinforcementLearning
from utils.config import Config

def main():
    # Load historical stock data
    data_loader = DataLoader()
    historical_data = data_loader.load_data()

    # Initialize the neural network
    neural_network = NeuralNetwork()
    
    # Train the trading agent
    trading_agent = TradingAgent(neural_network)
    reinforcement_learning = ReinforcementLearning(trading_agent)
    reinforcement_learning.train(historical_data)

    # Simulate market conditions
    market_simulator = MarketSimulator()
    simulated_data = market_simulator.simulate_market()

    # Execute paper trading
    paper_trader = PaperTrader(trading_agent)
    paper_trader.execute_trades(simulated_data)

if __name__ == "__main__":
    main()