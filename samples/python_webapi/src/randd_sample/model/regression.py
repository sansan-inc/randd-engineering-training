import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin


class LinearRegression(BaseEstimator, RegressorMixin):
    def fit(self, X, y):
        self.coef_ = np.linalg.solve(np.dot(X.T, X), np.dot(X.T, y))
        return self

    def predict(self, X):
        return np.dot(X, self.coef_)
