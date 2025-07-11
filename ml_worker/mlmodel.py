import joblib

class MLmodel:

    def __init__(self):
        self.__model= joblib.load('./shared/xgboost_model.pkl')

    @property
    def model(self):
        return self.__model

    