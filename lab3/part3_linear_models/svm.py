import numpy as np

def svm(X, y):
    '''
    SVM Support vector machine.

    INPUT:  X: training sample features, P-by-N matrix.
            y: training sample labels, 1-by-N row vector.

    OUTPUT: w: learned perceptron parameters, (P+1)-by-1 column vector.
            num: number of support vectors

    '''
    P, N = X.shape
    w = np.zeros((P + 1, 1))
    num = 0

    # YOUR CODE HERE
    # Please implement SVM with scipy.optimize. You should be able to implement
    # it within 20 lines of code. The optimization should converge wtih any method
    # that support constrain.
    #TODO
    # begin answer

    from scipy.optimize import minimize

    X_aug = np.vstack([np.ones((1,N)) , X])
    w0 = np.zeros(P + 1)

    def objective (w):
        return 0.5 * np.sum(w[1:] ** 2)
    
    constraints = []
    for i in range(N):
        constraints.append({
            'type':'ineq',
            'fun':lambda w, i=i: y[0,i] * (w.T @ X_aug[:,i]) -1
        })

    result = minimize(objective, w0, method='SLSQP', constraints=constraints)

    w = result.x.reshape(-1,1)

    num = 0
    for i in range(N):
        if np.abs(y[0,i] * (w.T @ X_aug[:,i]) -1 ) < 1e-3:
            num += 1 

    # end answer
    return w, num

