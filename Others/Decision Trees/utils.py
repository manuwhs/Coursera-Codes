

import numpy as np

def get_ftype(X):
    # Detects the type of one dimensional array
    ftype = type(X[0]).__name__
    
    # Check if it is categorical
    if (ftype == "int64"):
        return 1
    elif(ftype == "string_"):
        return 1
    
    return 0
    
def get_types(X):
    # Detect Categorical and Numeric Features

    # X = np.array(Nsamples, Nfeatures)
    
    Nsa, Ndim = X.shape
    ftype = np.zeros((Ndim,1), dtype = "int64")  # Vector with the types
    
    for d in range(Ndim):
        typ = get_ftype(X[:,d])
        ftype[d] = typ
        
    return ftype

def unique(array,return_counts=True):
    # Implementation  of the new features of unique taht for some reason I dont have
    unicos = np.unique(array)
    
    if(return_counts==True):
        counts = []
        array_l = list(array)
        for uniq in unicos:
            counts.append(array_l.count(uniq))
        
    return unicos, np.array(counts)
    
def entropy(dataLabels):
    """
    Calculate Shannon entropy
    :dataLabels: Labels of the samples to calculate entropy
    :return: a float representing the Shannon entropy
    """
    # Calculate frequency of the labels
    _, val_freqs = unique(dataLabels, return_counts=True)
#    print dataLabels
#    print val_freqs
    # Calculate probabilities of the labels normalizing
    
    val_probs = val_freqs / float(len(dataLabels))
#    print val_probs
    return -val_probs.dot(np.log(val_probs))
    
def info_gain(dataLabels, labelsTr):
    
    # Information gain if we split the dataLabels samples using the labelsTr
    # We calculate the entropy of the whole samples dataLabels
    # Then we calculate the entropy of datalbels conditioned to the labelsTr
    #   We split the dataLabels into len(unique(labelsTr)) groups and compute the entropy of those gropus
    # for training in labels_tr
    """
    Calculate information gain
    :param dataLabels: Labels of the training data
    :param labels:    Partition of the training data in the node
    """
    ### Initial entropy before partition
    Hs = entropy(dataLabels)
#    print "Entropy: " + str(Hs)
    # Calculate probabilities of the labels n
    labelsTr_unique, val_freqs = unique(labelsTr, return_counts=True)
#    print labelsTr_unique
    val_probs = val_freqs / float(len(dataLabels))
    
    EA = 0.0
    for  i in range(len(labelsTr_unique)):
        lTr = labelsTr_unique[i]
#        print lTr
#        print labelsTr
        class_indxes = np.where(labelsTr == lTr)[0]
#        print class_indxes
        Hs_i = entropy(dataLabels[class_indxes])
#        print "Entropi Cond: " + str(Hs_i)
        EA += val_probs[i] * Hs_i

#    print Hs,EA
    return Hs - EA 
        
        
from sklearn.preprocessing import LabelEncoder
import copy
## Multicolumn Label Encoder because LabelEncoder only does it for one variable
class MultiColumnLabelEncoder:
    def __init__(self,X = None):
        self.X = X  # array of column names to encode
        self.LabelEncoders = []   # One label encoder per column
        
    def fit(self,X = None):
        self.X = X
        self.LabelEncoders = []
        
        Nsa, self.Ndim = self.X.shape
        for d in range(self.Ndim):
            LE = LabelEncoder().fit(X[:,d])  # Train the single label encoder for 1 variable
            self.LabelEncoders.append(copy.deepcopy(LE))
            
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        out = []
        for d in range(self.Ndim):
            outLE = self.LabelEncoders[d].transform(X[:,d])  # Train the single label encoder for 1 variable
            out.append(outLE)
        
        out = np.array(out).T  # Transform to numpy and transpose
        return out

    def fit_transform(self,X):
        return self.fit(X).transform(X)






















def train_test_splitk (X, Y, train_ratio):
    
####################################################################
#################### SPLIT TRAIN TEST data #########################
#################################################################
    order = np.arange(np.shape(X)[0],dtype=int) # Create array of index
    order = np.random.permutation(order)        # Randomize the array of index
    
    Ntrain = round(train_ratio*np.shape(X)[0])    # Number of samples used for training
    Ntest = len(order)-Ntrain                  # Number of samples used for testing
    Xtrain = X[order[:Ntrain]]
    Xtest = X[order[Ntrain:]]
    Ytrain = Y[order[:Ntrain]]
    Ytest = Y[order[Ntrain:]]
    
    return Xtrain, Xtest, Ytrain, Ytest