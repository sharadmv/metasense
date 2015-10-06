import GPy
import numpy as np
from cf import Classifier

class GPClassifier(Classifier):

    def __init__(self, length_scale=0.1):
        super(GPClassifier, self).__init__()
        self._model = []
        self.length_scale = 0.1

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
        kernel = GPy.kern.RBF(input_dim=5, lengthscale=self.length_scale)
        for d in xrange(ytrain.shape[1]):
            self._model.append(GPy.models.SparseGPRegression(xtrain, np.matrix(ytrain[:, d]).T, kernel))

    def predict(self, x):
        (date, x) = x
        x = x.as_matrix()
        prediction = []
        for d in xrange(len(x)):
            prediction.append(self._model[d].predict(np.array([x]))[0][0][0])
        return np.array(prediction)

