# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np   # Numeric Libraries
import scipy.io 
from sklearn import preprocessing

# For splitting data in train and test if necesary
from sklearn.cross_validation import train_test_split  


import DecisionTree as DT  # Decision Tree Library
import utils as ul         # Utility functions

#################################################
################# LOAD DATASET ##################
#################################################
dataset_folder = "./data/"
mat = scipy.io.loadmat(dataset_folder +'ionosfera.mat')
Xtrain = mat["X_tr"]
Ytrain = mat["T_tr"]
Xtest = mat["X_tst"]
Ytest = mat["T_tst"]

#Xtrain, Xtest, Ytrain, Ytest = train_test_split (X, Y, train_ratio = 0.6)

#################################################################
#################### DATA PREPROCESSING #########################
#################################################################

Ytrain = Ytrain.flatten()
Ytest = Ytest.flatten()

## Separate Categorical and Numeric Variables
fType = ul.get_types(Xtrain).flatten()  # Get the type of the features
#fType[0] = 1    # I know it is categorical
indxNum = np.where(fType == 0)[0]  # Indexes of the features that are numeric
indxCat = np.where(fType == 1)[0]  # Indexes of the features that are categorical

nNum = len(indxNum)
nCat = len(indxCat)

#%% Normalize Numeric data and transform categorical values to Integer numbers

if (nNum > 0):   # If we have numerical variables
    XtrNum = Xtrain[:,indxNum]  # Numerical Features
    scalerNum = preprocessing.StandardScaler().fit(XtrNum)
    
    XtrainNumNorm = scalerNum.transform(XtrNum)   # Training features normalized
    XtestNumNorm = scalerNum.transform(Xtest[:,indxNum])# Testing features normalized


if (nCat > 0):   # If we have categorical variables
    XtrCat = Xtrain[:,indxCat]  # Categorical Features
    scalerCat = ul.MultiColumnLabelEncoder().fit(XtrCat)

    XtrainCatNorm = scalerCat.transform(XtrCat)   # Training features normalized
    XtestCatNorm = scalerCat.transform(Xtest[:,indxCat])# Testing features normalized

if (nNum > 0 and nCat == 0):
    Xtrain = XtrainNumNorm
    Xtest = XtestNumNorm
    
elif (nCat > 0 and nNum == 0):
    Xtrain = XtrainCatNorm
    Xtest = XtestCatNorm

elif (nCat > 0 and nNum > 0):
    Xtrain = np.concatenate((XtrainNumNorm,XtrainCatNorm),axis = 1)
    Xtest = np.concatenate((XtestNumNorm,XtestCatNorm),axis = 1)

#fType[0] = 0  # Because I do it wrong
#fType[7] = 1


## TODO: Reorder the position of features to the original positions

#################### Call the Classifier and implement it ##########
from sklearn import tree
clf = tree.DecisionTreeClassifier(criterion = "entropy")
clf = clf.fit(Xtrain, Ytrain)
Ttest = clf.score(Xtest,Ytest)

######## It is out turn noww ############3
#print fType[2]

#fType =[0, 1]
#Xtrain = Xtrain[:,0:7]
#Ytrain = Ytrain[:]
#Xtest = Xtest[:,0:7]
#Ytest = Ytest[:]

myDT = DT.CDecisionTree()
myDT.fit(Xtrain,Ytrain,fType)
#myDT.plot_tree()

#Lab = myDT.predict(Xtrain)
print myDT.score(Xtrain,Ytrain)
print myDT.score(Xtest,Ytest)
## TODO !! Errors due to same values


