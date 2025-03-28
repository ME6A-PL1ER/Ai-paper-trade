class RewardFunctions:
    def __init__(self):
        pass

    def reward_for_profit(self, profit):
        """Calculate reward based on profit."""
        return profit

    def reward_for_holding(self, holding_period):
        """Calculate reward for holding a position."""
        return holding_period * 0.1  # Example: reward for each time step held

    def total_reward(self, profit, holding_period):
        """Calculate total reward based on profit and holding period."""
        return self.reward_for_profit(profit) + self.reward_for_holding(holding_period)

    def penalty_for_short_trades(self, trade_duration):
        """Apply a penalty for trades that are too short."""
        if trade_duration < 1:  # Example threshold for short trades
            return -1  # Penalty for short trades
        return 0

    def evaluate_trade(self, profit, holding_period, trade_duration):
        """Evaluate a trade and return the final reward."""
        reward = self.total_reward(profit, holding_period)
        penalty = self.penalty_for_short_trades(trade_duration)
        return reward + penalty