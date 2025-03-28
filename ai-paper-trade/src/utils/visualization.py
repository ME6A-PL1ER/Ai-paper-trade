from matplotlib import pyplot as plt

def plot_trading_performance(dates, portfolio_values, title="Trading Performance"):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, portfolio_values, label='Portfolio Value', color='blue')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.grid()
    plt.show()

def plot_model_predictions(dates, actual_prices, predicted_prices, title="Model Predictions"):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, actual_prices, label='Actual Prices', color='green')
    plt.plot(dates, predicted_prices, label='Predicted Prices', color='red')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()