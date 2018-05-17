from sklearn.preprocessing.data import minmax_scale 
import numpy as np
X = np.array([[ 10., -1.,  4.],
              [ 2.,  0., 5.],
              [ 0.,  0., -1.]])
# min_max_scaler = preprocessing.MinMaxScaler()
# X_minMax = min_max_scaler.minmax_scale(X)
for i in X:
    X_minMax = minmax_scale(i)
    print(X_minMax )
