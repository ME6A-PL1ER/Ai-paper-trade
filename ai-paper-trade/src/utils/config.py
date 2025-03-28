# ai-paper-trade/src/utils/config.py

# Configuration settings for the Ai-paper-trade project

class Config:
    # API keys and tokens
    YFINANCE_API_KEY = "your_yfinance_api_key_here"
    
    # Trading parameters
    INITIAL_CAPITAL = 10000  # Starting capital for paper trading
    TRADE_SIZE = 100  # Size of each trade
    HOLDING_PERIOD = 5  # Number of days to hold a position

    # Model hyperparameters
    LEARNING_RATE = 0.001
    EPOCHS = 100
    BATCH_SIZE = 32

    # Reinforcement learning parameters
    DISCOUNT_FACTOR = 0.99  # Discount factor for future rewards
    EXPLORATION_RATE = 1.0  # Initial exploration rate
    EXPLORATION_DECAY = 0.995  # Decay rate for exploration
    MIN_EXPLORATION_RATE = 0.01  # Minimum exploration rate

    # Logging settings
    LOGGING_LEVEL = "INFO"  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOGGING_FILE = "trading_log.txt"  # Log file name

    # Other settings
    SIMULATION_SPEED = 100  # Speed of market simulation (e.g., 100x)
    HISTORICAL_DATA_PATH = "data/historical/"  # Path to historical data files