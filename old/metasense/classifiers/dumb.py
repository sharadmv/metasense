import pandas as pd
from cf import Classifier

class MeanClassifier(Classifier):

    def __init__(self):
        super(MeanClassifier, self).__init__()
        self._mean = None

    def fit(self, X):
        self._mean = X.mean()

    def predict(self, x):
        return self._mean

class MonthClassifier(Classifier):

    def __init__(self):
        super(MonthClassifier, self).__init__()
        self._months = {}

    def fit(self, X):
        months = X.groupby(pd.TimeGrouper('1M')).transform(lambda x: x.mean())
        for date, x in months.iterrows():
            self._months[date.to_datetime().month] = x

    def predict(self, x):
        (date, row) = x
        month = date.to_datetime().month
        return self._months[month]
