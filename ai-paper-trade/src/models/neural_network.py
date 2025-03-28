class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = self.initialize_weights(input_size, hidden_size)
        self.weights_hidden_output = self.initialize_weights(hidden_size, output_size)

    def initialize_weights(self, input_size, output_size):
        return np.random.randn(input_size, output_size) * 0.01

    def forward(self, x):
        self.hidden_layer_activation = np.dot(x, self.weights_input_hidden)
        self.hidden_layer_output = self.activation_function(self.hidden_layer_activation)
        self.output_layer_activation = np.dot(self.hidden_layer_output, self.weights_hidden_output)
        return self.output_layer_activation

    def activation_function(self, x):
        return 1 / (1 + np.exp(-x))  # Sigmoid activation function

    def train(self, x, y, learning_rate, epochs):
        for epoch in range(epochs):
            output = self.forward(x)
            loss = self.calculate_loss(y, output)
            self.backpropagation(x, y, output, learning_rate)

    def calculate_loss(self, y_true, y_pred):
        return np.mean((y_true - y_pred) ** 2)  # Mean Squared Error

    def backpropagation(self, x, y, output, learning_rate):
        output_error = y - output
        output_delta = output_error * self.activation_derivative(output)

        hidden_layer_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_layer_delta = hidden_layer_error * self.activation_derivative(self.hidden_layer_output)

        self.weights_hidden_output += self.hidden_layer_output.T.dot(output_delta) * learning_rate
        self.weights_input_hidden += x.T.dot(hidden_layer_delta) * learning_rate

    def activation_derivative(self, x):
        return x * (1 - x)  # Derivative of the sigmoid function