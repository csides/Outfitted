import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.decomposition import NMF


def MatrixFactorization(R, numfeats, steps, alpha, beta):
    numusers = R.shape[0]
    numitems = R.shape[1]
    P = np.random.randn(numusers,numfeats) / 3. + 0.5
    Q = np.random.randn(numfeats,numitems) / 3. + 0.5
    for step in xrange(steps):
        for i in xrange(numusers):
            for j in xrange(numitems):
                if not np.isnan(R[i][j]):
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    for k in xrange(numfeats):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        #eR = np.dot(P,Q)
        if step%10==0:
            esqr = 0
            for i in xrange(numusers):
                for j in xrange(numitems):
                    if not np.isnan(R[i][j]):
                        diff = R[i][j] - np.dot(P[i,:],Q[:,j])
                        esqr += diff * diff
                        esqr += beta * (np.dot(P[i,:],P[i,:]) + np.dot(Q[:,j],Q[:,j]))
            e = np.sqrt(esqr)
            if e < 0.001:
                return P, Q
            print step, e
        
        if step%100==0:
            print "P"
            print P
            print "Q"
            print Q
            print "R_hat"
            print np.dot(P,Q)
        
    return P,Q

def convert12_to_10(x):
    if x == 1.:
        return 1.
    elif x == 2.:
        return 0.
    return x
convert12_to_10 = np.vectorize(convert12_to_10)

if __name__ == "__main__":
    data = convert12_to_10( np.genfromtxt('Data Set 2.csv',delimiter=',',skip_header=2) )
    print data
    
    numusers, numitems = data.shape
    
    print numusers
    print numitems
    
    P,Q = MatrixFactorization(data, 5, 5000, 0.01, 0.01)
    prediction = np.dot(P,Q)
    
    print data
    print prediction








