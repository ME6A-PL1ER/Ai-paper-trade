# Ai-paper-trade

## Overview

Ai-paper-trade is a project aimed at simulating stock trading using reinforcement learning techniques. The goal is to train a neural network to make trading decisions based on historical stock data and simulate trades in a risk-free environment.

## Project Structure

The project is organized into several directories and files:

- **src/**: Contains the main application code.
  - **main.py**: Entry point of the application.
  - **data/**: Handles data loading and preprocessing.
    - **data_loader.py**: Class for loading historical stock data using yfinance.
    - **yfinance_api.py**: Wrapper around the yfinance library for fetching stock data.
  - **models/**: Contains the neural network and trading agent.
    - **neural_network.py**: Defines the architecture of the neural network.
    - **trading_agent.py**: Interacts with the neural network to make trading decisions.
  - **simulation/**: Simulates market conditions and trading.
    - **market_simulator.py**: Simulates market conditions and generates synthetic data.
    - **paper_trader.py**: Simulates executing trades based on the trading agent's decisions.
  - **trading/**: Implements trading strategies and broker interactions.
    - **strategy.py**: Implements various trading strategies.
    - **broker_interface.py**: Interface for interacting with a brokerage API.
  - **utils/**: Contains utility functions and configuration settings.
    - **config.py**: Configuration settings for the project.
    - **visualization.py**: Functions for visualizing trading performance.
  - **training/**: Implements reinforcement learning algorithms.
    - **reinforcement_learning.py**: Trains the trading agent based on the reward system.
    - **reward_functions.py**: Defines reward functions for evaluating performance.

- **data/**: Contains directories for storing historical data.
  - **historical/**: Directory for historical stock data.

- **notebooks/**: Contains Jupyter notebooks for exploratory data analysis.
  - **exploration.ipynb**: Notebook for experimentation with models and strategies.

- **tests/**: Contains unit tests for the application.
  - **test_data_loader.py**: Tests for data loading functionality.
  - **test_models.py**: Tests for the neural network and trading agent.
  - **test_simulation.py**: Tests for market simulation and paper trading.

- **requirements.txt**: Lists the dependencies required for the project.

- **setup.py**: Used for packaging the project.

- **.gitignore**: Specifies files and directories to ignore in version control.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-paper-trade
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the project settings in `src/utils/config.py`.

4. Run the main application:
   ```
   python src/main.py
   ```

## Usage Guidelines

- Use the `notebooks/exploration.ipynb` for exploratory data analysis and to experiment with different models and strategies.
- Modify the trading strategies in `src/trading/strategy.py` to test different approaches.
- Implement and test new reward functions in `src/training/reward_functions.py` to improve the training process.

## Future Work

- Improve the neural network architecture for better prediction accuracy.
- Implement more sophisticated trading strategies.
- Explore additional data sources for enhanced training data.