import numpy as np
from joblib import Parallel, delayed

class MulticlassSVM:
    def __init__(self, n_classes, learning_rate=0.001, lambda_param=0.01, n_iters=1000, n_jobs=-1):
        self.n_classes = n_classes
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.classifiers = []
        self.n_jobs = n_jobs

    def train_classifier(self, class_idx, X, y):
        binary_y = np.where(y == class_idx, 1, -1)
        svm_classifier = BinarySVM(self.lr, self.lambda_param, self.n_iters)
        svm_classifier.fit(X, binary_y)
        return svm_classifier

    def fit(self, X, y):
        self.classifiers = Parallel(n_jobs=self.n_jobs)(delayed(self.train_classifier)(class_idx, X, y) for class_idx in range(self.n_classes))

    def predict(self, X):
        class_scores = np.zeros((len(X), self.n_classes))

        for idx, classifier in enumerate(self.classifiers):
            class_scores[:, idx] = classifier.decision_function(X)

        return np.argmax(class_scores, axis=1)

class BinarySVM:
    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape

        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y[idx] * (np.dot(x_i, self.weights) - self.bias) >= 1
                if condition:
                    self.weights -= self.lr * (2 * self.lambda_param * self.weights)
                else:
                    self.weights -= self.lr * (2 * self.lambda_param * self.weights - np.dot(x_i, y[idx]))
                    self.bias -= self.lr * y[idx]

    def decision_function(self, X):
        return np.dot(X, self.weights) - self.bias
 