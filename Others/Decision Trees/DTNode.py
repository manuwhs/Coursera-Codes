# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy
import utils as ul
    
class CDTNode():
    # Elemtary table of Key-value entries.
    # The list of keys is unordered

    def __init__(self, depth):  #create an empty priority queue

        self.tr_indx = []  # Indexes of the training samples that get to the node
        self.depth = depth
    ############# Set dividing functions ##############
    ## Given a Rule, we want to divide a given set into the ones that divide it into
    ## One set and the other.
    
    def build(self, X, Y, ftype):  # Build given X,Y and ftype of features
        self.X = X
        self.Y = Y
        self.ftype = ftype
        
        self.Nsa, self.Ndim = X.shape
    
        self.nodeLabel = None  # If it is not equal to None, then this is a final output
        self.features = []  # Features to use in this node
        self.parameters = []  # Parameters to use in the split.
        self.subcategories = None # Category of the child nodes
        self.childNodes = []    # List of child nodes
        
        print "----------------------"
        print "Building node"
        print "Samples: " + str(self.Nsa)

        for i in range(self.Ndim):
            self.parameters.append([])
            # For example if the feature is continouus we need a threshold
        
        ################################################################
        ########## Check if this node is good enough ###################
        #################################################################
        output_types, freq =  ul.unique(self.Y)
        
        self.freq = freq
        print "Freq: " + str(freq)
        if (len(output_types) == 1):  # If the set only contains a type
            
            self.nodeLabel = output_types[0]   # Set it as the type
            return 1
            
        if (self.Nsa == 0):  # If we have no samples (when diving in categorical values and we dont have of one class)

            self.nodeLabel = 0   # Set it as the type we dont know
            return 1
            
        ################################################################
        ########## If we have to keep splitting ###################
        #################################################################
        # Chose the best feature
        best_d = self.choose_best_attribute()
        if (best_d == -1):   # If we cannot split because there same samples X with different Y
            # We set this node as an end node and stablish its value as the majority class
            self.nodeLabel = output_types[np.argmax(freq)]  # Most class
            return 1
            
        print "Threshold: " + str(self.parameters)
        # Get the child labels from this node
        labels = self.classify(self.X)
        
        output_types, freq =  ul.unique(labels)
        print "Child labels freq " + str(freq)
#        print labels
        # Split the data according to the feature and create children
        for cn in self.subcategories:  # For every child node
            cn_indexes = np.where(labels == cn)[0]   # indexes of samples going to the child node
            # Create the child node and build again until some criterion meet
            childNode = CDTNode(depth = self.depth + 1)
            childNode.build(self.X[cn_indexes,:],self.Y[cn_indexes],self.ftype)
            self.childNodes.append(copy.deepcopy(childNode))
            
    def classify(self,X):
        # This function gets the label of the child nodes for this trained node
        Nsa,Ndim = X.shape
        if (self.ftype[self.features] == 0):  # If this node has a numeric feature
            
            labels = X[:,self.features] > self.parameters   # We just check wether it is bigger or smaller
#            print labels
        elif(self.ftype[self.features] == 1): # if categorical
            # We have to select the node whose corresponding label is this one
            # The node has its label in paramters
            labels = np.zeros((Nsa,1))
            for i in range(len(self.subcategories)): # For every child node (1 child = 1 category)
                # We check the category of every sample and get the index of its node
                sel = X[:,self.features] == self.subcategories[i]
                sel = np.array(sel)
                print sel.shape
                print labels.shape
                
                labels[:,0] += sel.T*i
            
        return labels
        
    def predict(self, X):  
        """
        Make predictions for the rows passed in data
        :param data: rows of attribute values
        :return: a numpy array of labels
        """
        ## It predicts the labels recursively givings them to the lower nodes
        
        
        if (X.size == 0):  # If empty data
            return

        # Convert to 2-D array (Nsa, Ndim) in case there is only one dimension and it is (Nsam,)
        if len(X.shape) == 1: # 
            X = np.reshape(X, (1,len(X)))

        if (self.nodeLabel != None):
            # If we're at the bottom of the tree then return the labels for all records as the tree node label
            labels = np.ones(len(X)) * self.nodeLabel
#            print self.nodeLabel
            return labels

        # If we are not at the bottom of the tree
        labels = np.zeros(len(X))  # Final labels to return
        childLabels = self.classify(X)  # Labels of the children
        
        for i in range(len(self.childNodes)):  # For every child node
            # Get the array indexes where the split attibute value  = child attribute value
            sel_samples = childLabels == i
            labels[sel_samples] = self.childNodes[i].predict(X[sel_samples,:])
            

        return labels
        
    def choose_best_attribute(self):
        """
        Choose an attribute to split the children on
        :param data: values for all attributes
        :param labels: values for corresponding labels
        :param attributes: attribute columns
        :param fitness: the closeness of fit function
        :return: empty ... self.attribute will be set by this function instead
        """
        best_gain = float('-inf')
   
        for d in range(self.Ndim):  # For every feature
        
            gain = self.get_gain(self.X, self.Y, d)
            print "Gain Feature " + str(d) + " " + str(gain)
            if gain > best_gain:
                best_gain = gain
                self.features = d
            
        if (best_gain == 0):
            # IF the gain is 0 because there are samples with same X and different Y that can not be differentiated
            # We end the node basically
            return -1
            
        if (self.ftype[self.features] == 0):
            # If we have a numerical input
            self.parameters = self.parameters[self.features]  # Set the parameters as the threshols
            self.subcategories = [0,1]
        else:  # If it is numerical, this will be an array with the values of the categories of the child nodes
            self.subcategories = np.unique(self.X[:,self.features])
            self.parameters = 1
        print "Best Gain " + str(self.features) + ", Th: " + str(self.parameters)
        return d
     
    def get_gain(self,X,Y,d):
         # Gets the informationd gain of using feature X for discrimination
         # ftype is for knowing if the feature is categorial or numerical
#        print self.ftype[d]
#        print d
        ftype = self.ftype[d]

        if (ftype == 0):
            gain = self.get_numericalGain(d)
        elif (ftype == 1):
            gain = self.get_categoricalGain(d)
        
        return gain
        
    def get_numericalGain(self,d):
        # Gets the gain of using feature X to partition the samples
        # It tries all the possible thresholds for that feature 
        X = self.X[:,d]
        Y = self.Y
        order = np.argsort(X)
        Xsorted = X[order]
        Ysorted = Y[order]
        # Get the info gain for every possible threshold between samples
#        print Xsorted
        Bestgain = float("-inf")
        
        
        method_sel = 0
        ################1Method 1 for divisions #######################3
        Ncuts = 0
        if (method_sel == 1):
            for i in range(1, Ncuts):
                indx = int((i)* (self.Nsa/float(Ncuts)))
                Yselected_sorted = X > Xsorted[indx]
                gain = ul.info_gain(Ysorted,Yselected_sorted)
        
                if(gain > Bestgain):
                    Bestgain = gain
                    threshold = (Xsorted[indx-1] + Xsorted[indx])/2
    #                print "Found better T: "+ str(i) +", " + str(threshold)
                    best_i = i
        else:
            for i in range(1,self.Nsa):  # For every sample
                # Get the output of the classified values in terms of 
    #            if (i > 1):  ## Detect duplciates1
                if (Xsorted[i] == Xsorted[i-1]):
                    continue;
    #            if (i < self.Nsa -1):  ## Detect duplciates
    #                if (Xsorted[i] == Xsorted[i+1]):
    #                    continue;
    #                    
                Yselected_sorted = [0]*i
                Yselected_sorted.extend([1]*(self.Nsa-i))
    
    #            print Yselected_sorted
    #            print Ysorted
                
                gain = ul.info_gain(Ysorted,Yselected_sorted)
        
                if(gain > Bestgain):
                    Bestgain = gain
                    threshold = (Xsorted[i-1] + Xsorted[i])/2
    #                print "Found better T: "+ str(i) +", " + str(threshold)
                    best_i = i
        
        if (Bestgain == float("-inf")):  # If all the samples are the same
            Bestgain = 0    # We exit with 0
            return Bestgain
                
        self.parameters[d] = threshold
#        print Xsorted
#        print np.sum(X > threshold), best_i, np.sum(Yselected_sorted)
#        print "Trying " + str(d) + " : Gain " + str(Bestgain)+ " Th : " + str(threshold)
#        if (np.sum(X > threshold) > best_i):
            
        return Bestgain
        
    def get_categoricalGain(self,d):
        X = self.X[:,d]
#        print "La X"
#        print X
        Y = self.Y
        # We just partition it into all possible categories
        Gain = ul.info_gain(Y,X)
        
        print "Gain "+str(d) + ": "+str(Gain)
        return Gain