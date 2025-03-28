class MarketSimulator:
    def __init__(self, historical_data):
        self.historical_data = historical_data
        self.current_index = 0
        self.current_price = self.historical_data[self.current_index]

    def step(self):
        if self.current_index < len(self.historical_data) - 1:
            self.current_index += 1
            self.current_price = self.historical_data[self.current_index]
            return self.current_price
        else:
            return None  # End of data

    def reset(self):
        self.current_index = 0
        self.current_price = self.historical_data[self.current_index]
        return self.current_price

    def get_current_price(self):
        return self.current_price

    def simulate_market_conditions(self):
        # This method can be expanded to simulate various market conditions
        pass