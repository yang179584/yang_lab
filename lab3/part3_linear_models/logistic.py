import numpy as np

def logistic(X, y):
    '''
    LR Logistic Regression.

    INPUT:  X: training sample features, P-by-N matrix.
            y: training sample labels, 1-by-N row vector.

    OUTPUT: w: learned parameters, (P+1)-by-1 column vector.
    '''

    P, N = X.shape
    X_aug = np.vstack([np.ones((1,N)) , X])
    y = y.T

    w = np.zeros((P + 1, 1))
    # YOUR CODE HERE
    # begin answer

    learning_rate = 0.01
    num = 1000
    tolerance = 1e-6

    for i in range (num):
        z = X_aug.T @ w
        y_pre = 1 / (1 + np.exp(-z))

        gradient = ( X_aug @ (y_pre - y)) / N
        w = w - learning_rate * gradient

        if np.linalg.norm(gradient) < tolerance:
            break

    # end answer
    return w
