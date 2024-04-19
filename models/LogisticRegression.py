import numpy as np
class LogisticRegression:
    def __init__(self, learning_rate=0.01, num_iterations=1000, regularization=None, reg_param=0.01):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.regularization = regularization
        self.reg_param = reg_param
        self.weights = None
        self.bias = None
        self.classes = None

    def softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def cross_entropy_loss(self, y_true, y_pred):
        m = y_true.shape[0]
        loss = -np.sum(y_true * np.log(y_pred + 1e-15)) / m
        return loss

    def fit(self, X, y):
        self.classes = np.unique(y)
        num_features = X.shape[1]
        num_classes = len(self.classes)

        # Initialize weights and bias
        self.weights = np.zeros((num_features, num_classes))
        self.bias = np.zeros(num_classes)
        y = np.eye(num_classes)[y]
        for _ in range(self.num_iterations):
            # Forward pass
            z = np.dot(X, self.weights) + self.bias
            y_pred = self.softmax(z)

            # Compute gradients
            dz = y_pred - y
            dw = np.dot(X.T, dz)
            db = np.sum(dz, axis=0)

            # Add regularization
            if self.regularization == 'l2':
                dw += self.reg_param * self.weights
            elif self.regularization == 'l1':
                dw += self.reg_param * np.sign(self.weights)

            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict_proba(self, X):
        z = np.dot(X, self.weights) + self.bias
        return self.softmax(z)

    def predict(self, X):
        probabilities = self.predict_proba(X)
        return np.argmax(probabilities, axis=1)