from train_model import ModelRunner
import numpy as np
import pandas as pd


class Signals:
    def __init__(self, model, low_threshold = 0.3, high_threshold=0.7):
        self.model = model
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.signals = {}


    def generate(self, X):
        if isinstance(X, (pd.Series, pd.DataFrame)):
            X = X.values
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        probas = self.model.predict_proba(X)[:, 1]
        signals = np.where(probas >= self.high_threshold, "SELL", np.where(probas <= self.low_threshold, "BUY", "HOLD"))
        return {"probabilities": probas.tolist(), "signals": signals.tolist()}

