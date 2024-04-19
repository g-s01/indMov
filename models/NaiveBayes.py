import numpy as np

class GNB:
    def fit(self, X, y, smoothing_value = 1e-9):
        self.classes = np.unique(y)
        self.n_classes = len(self.classes)
        self.mean = np.zeros((self.n_classes, X.shape[1]))
        self.var = np.zeros((self.n_classes, X.shape[1]))
        self.prior = np.zeros(self.n_classes)
        self.epsilon = smoothing_value * np.var(X, axis=0).max()
        for idx, c in enumerate(self.classes):
            X_c = X[y == c]
            self.mean[idx, :] = X_c.mean(axis=0)
            self.var[idx, :] = X_c.var(axis=0) + self.epsilon
            self.prior[idx] = X_c.shape[0] / float(len(y))
    
    def predict(self, X):
        posteriors = []
        
        for idx, c in enumerate(self.classes):
            prior = np.log(self.prior[idx])
            posterior = np.sum(np.log(self._pdf(idx, X)), axis=1)
            posterior = prior + posterior
            posteriors.append(posterior)
        
        posteriors = np.array(posteriors).T
        return self.classes[np.argmax(posteriors, axis=1)]
    
    def _pdf(self, class_idx, X):
        mean = self.mean[class_idx]
        var = self.var[class_idx]
        numerator = np.exp(-((X - mean) ** 2) / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator
