from pathlib import Path

import joblib
import numpy as np


class RegressionService:
    model = None

    @classmethod
    def get_model(cls):
        if cls.model is None:
            cls.model = joblib.load(Path(__file__).parent.joinpath("model", "pkl", "sample.pkl"))
        return cls.model

    @classmethod
    def predict(cls, request):
        return cls.get_model().predict(cls.dict_to_array(request))

    @staticmethod
    def dict_to_array(dict_request):
        keys = [
            "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE",
            "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"
        ]
        return np.array([dict_request[k] for k in keys])
