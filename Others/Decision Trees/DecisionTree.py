# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy
from DTNode import CDTNode
import pydot

class CDecisionTree():
    # Decision Tree classifier !!

    def __init__(self, root = None):  #create an empty priority queue
        if (root == None):
            self.root = CDTNode(depth = 1)
        
        
        ## Elementary properties
        self.X = []   # Training Samples
        self.T = []   # Labels of Training Samples
        
        
        self.maxDepth = 1000   # Depth of the tree
        self.criterion = "Entropy"  # Criterion function to choose the attributes
        self.decisionF = "stump"    # Decision function to be used at nodes
        
    def fit(self,X,T,ftype):  # Trains the network using the training data X,T
        self.root.build(X,T,ftype)
        
    def plot_tree(self):
        
        # first you create a new graph, you do that with pydot.Dot()
        graph = pydot.Dot(graph_type='digraph')
        self.get_children_nodes(graph, None, self.root)
        graph.write_png('pen.png')

    def predict (self,X): #this function classifies X until the leaves
#        print "Prefiction"
        labels = self.root.predict(X)
        return labels
        
    def score(self,X,Y):
        labels = self.predict(X)
        
        nright = np.sum(np.equal(labels,Y))
        return nright/float(len(Y))
        
    def get_children_nodes(self, graph, parent_nodeg, node):
        # graph = total graph
        # Parent_nodeg = Graphical node of the parent
        ## Create a graphical node for this node.
        # If it is a leaf, we put the value -1 or 1
        # If not we put its th and d and call its children
        if (len(node.childNodes) == 0):  # If end node
            node_g = pydot.Node(str(np.random.uniform(0,1,10)), label = str(node.nodeLabel),shape='box')  # Create ndoe for the child
            graph.add_node(node_g)   # copy.deepcopy ??   # Add node to the structre
            graph.add_edge(pydot.Edge(parent_nodeg, node_g,
                        label = str(node.Nsa))) # Add edge
        else:
            node_g = pydot.Node(str(np.random.uniform(0,1,10)), 
                                label = "Depth:" + str(node.depth) + "\n" +\
                                "Var: " + str(node.features) + "\n" +\
                                "Freq: " + str(node.freq))  # Create ndoe for the child
            graph.add_node(node_g)   # copy.deepcopy ??   # Add node to the structre
            
            if (parent_nodeg != None):  # If we are not at the root
                graph.add_edge(pydot.Edge(parent_nodeg, node_g)) # Add edge
            
            for cn in node.childNodes:
                self.get_children_nodes(graph, node_g, cn)
            

