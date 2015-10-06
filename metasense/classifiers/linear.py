import sklearn
import numpy as np
from cf import Classifier

class LinearClassifier(Classifier):

    def __init__(self):
        super(LinearClassifier, self).__init__()
        self._model = sklearn.linear_model.LinearRegression()

    def fit(self, X):
        xtrain, ytrain = [], []
        length = len(X)
        for i, (date, x) in enumerate(X.iterrows()):
            if i == length - 1:
                continue
            xtrain.append(x.as_matrix())
            ytrain.append(X.iloc[i + 1].tolist())
        xtrain = np.array(xtrain)
        ytrain = np.array(ytrain)
        self._model.fit(xtrain, ytrain)

    def predict(self, x):
        return self._model.predict(x[1].as_matrix())[0]

class LassoClassifier(LinearClassifier):

    def __init__(self, alpha=0.1):
        super(LassoClassifier, self).__init__()
        self._model = sklearn.linear_model.Lasso(alpha=alpha)
