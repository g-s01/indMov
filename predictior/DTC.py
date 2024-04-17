class DTC:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.min_samples_split = 2
    def gini_impurity(y):
        n_samples = len(y)
        if n_samples == 0:
            return 0

        y_sorted = y[y[:, 0].argsort()]

        split_points = (y_sorted[:-1, 0] + y_sorted[1:, 0]) / 2

        min_gini = float('inf')
        best_split_point = None

        for split_point in split_points:
            left_indices = y_sorted[:, 0] <= split_point
            right_indices = ~left_indices

            left_gini = DTC.gini_impurity_helper(y_sorted[left_indices, 1])
            right_gini = DTC.gini_impurity_helper(y_sorted[right_indices, 1])

            weighted_gini = (len(y_sorted[left_indices]) * left_gini + len(y_sorted[right_indices]) * right_gini) / n_samples

            if weighted_gini < min_gini:
                min_gini = weighted_gini
                best_split_point = split_point
        return min_gini, best_split_point

    def gini_impurity_helper(y):
        
        n_samples = len(y)
        if n_samples == 0:
            return 0

        classes = np.unique(y)
        class_counts = np.zeros(len(classes))
        for i, c in enumerate(classes):
            class_counts[i] = np.sum(y == c)

        gini = 1.0
        for count in class_counts:
            gini -= (count / n_samples) ** 2

        return gini
    
    def fit(self, X, y):
        self.tree = self._grow_tree(X, y)
        # print(self.tree)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        n_classes = len(np.unique(y))
        if (self.max_depth is not None and depth >= self.max_depth) or n_classes == 1 or n_samples < self.min_samples_split:
            return {'class': np.bincount(y).argmax()}

        best_gini = float('inf')
        best_feature = None
        best_threshold = None
        for feature in range(n_features):
            data = X[:,feature]
            gini, threshold = DTC.gini_impurity(np.array([data, y]).T)
            if gini < best_gini:
                best_gini = gini
                best_feature = feature
                best_threshold = threshold

        left_indices = X[:, best_feature] <= best_threshold
        right_indices = X[:, best_feature] > best_threshold
        if y[left_indices].shape[0] == 0 or y[right_indices].shape[0] == 0:
            return {'class': np.bincount(y).argmax()}
        left_subtree = self._grow_tree(X[left_indices], y[left_indices], depth + 1)
        right_subtree = self._grow_tree(X[right_indices], y[right_indices], depth + 1)
        
        return {'feature': best_feature,
                'threshold': best_threshold,
                'left': left_subtree,
                'right': right_subtree}
    
    def predict(self, X):
        return np.array([self._predict_one(x, self.tree) for x in X])

    def _predict_one(self, x, tree):
        if 'class' in tree:
            return tree['class']
        feature = tree['feature']
        threshold = tree['threshold']
        if x[feature] <= threshold:
            return self._predict_one(x, tree['left'])
        else:
            return self._predict_one(x, tree['right'])
