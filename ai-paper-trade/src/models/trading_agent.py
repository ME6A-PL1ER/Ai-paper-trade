class TradingAgent:
    def __init__(self, neural_network):
        self.neural_network = neural_network

    def decide_action(self, current_data):
        prediction = self.neural_network.predict(current_data)
        action = self._interpret_prediction(prediction)
        return action

    def _interpret_prediction(self, prediction):
        if prediction > 0.5:
            return 'buy'
        elif prediction < -0.5:
            return 'sell'
        else:
            return 'hold'