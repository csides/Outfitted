import numpy as np

def build_sample_matrix(A, removeratio):
    shape = A.shape
    totalvals = sum(sum(np.logical_not(np.isnan(A))))
    numtoremove = int(totalvals * removeratio)
    
    choices = np.random.choice(totalvals, numtoremove, replace=False)
    choice_matrix = np.zeros_like(A, bool)
    sample_matrix = np.copy(A)
    index = 0
    for i in xrange(shape[0]):
        for j in xrange(shape[1]):
            if not np.isnan(A[i][j]):
                if index in choices:
                    sample_matrix[i][j] = np.nan
                    choice_matrix[i][j] = True
                index += 1
    return sample_matrix, choice_matrix

def test(predictor, data, numtrials, removeratio):
    '''
    'predictor' is a function that takes an incomplete subset of 'data' and returns
    a completed matrix of predicted values. 'samples' is the number of tests to
    run. 'numtestvals' is how many values are checked against the prediction per
    person in each test.
    This test removes 'numtestvals' from each row in data and runs predictor on
    this subset of the data. Error from actual data is calculated. This test
    is run 'samples' times and the mean and stddev of these test results
    is returned.
    '''
    results = []
    numusers, numitems = data.shape
    for trial in xrange(numtrials):
        sample_matrix, choice_matrix = build_sample_matrix(data, removeratio)
                    
        prediction = predictor(sample_matrix)
        
        esqr = 0.
        for i in xrange(numusers):
            for j in xrange(numitems):
                if choice_matrix[i][j]:
                    esqr += (data[i][j] - prediction[i][j]) ** 2
        e = np.sqrt(esqr)
        results.append(e)
    return np.mean(results), np.std(results)

from NNMF import convert12_to_10

if __name__ == "__main__":
    def random_predictor(M):
        return np.random.randint(0,2,M.shape)
    data = convert12_to_10( np.genfromtxt('Data Set 2.csv',delimiter=',',skip_header=2) )
    print test(random_predictor, data, 50, .2)


