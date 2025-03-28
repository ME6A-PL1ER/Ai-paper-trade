class ReinforcementLearning:
    def __init__(self, trading_agent, market_simulator, reward_function):
        self.trading_agent = trading_agent
        self.market_simulator = market_simulator
        self.reward_function = reward_function
        self.state = None
        self.total_reward = 0

    def reset(self):
        self.state = self.market_simulator.reset()
        self.total_reward = 0

    def step(self, action):
        next_state, reward, done = self.market_simulator.step(action)
        self.total_reward += reward
        self.trading_agent.learn(self.state, action, reward, next_state)
        self.state = next_state
        return next_state, reward, done

    def train(self, episodes):
        for episode in range(episodes):
            self.reset()
            done = False
            while not done:
                action = self.trading_agent.act(self.state)
                next_state, reward, done = self.step(action)
                if done:
                    print(f"Episode {episode + 1}: Total Reward: {self.total_reward}")

    def evaluate(self, num_episodes):
        total_rewards = []
        for episode in range(num_episodes):
            self.reset()
            done = False
            while not done:
                action = self.trading_agent.act(self.state)
                next_state, reward, done = self.step(action)
            total_rewards.append(self.total_reward)
        average_reward = sum(total_rewards) / num_episodes
        print(f"Average Reward over {num_episodes} episodes: {average_reward}")