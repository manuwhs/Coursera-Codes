# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import util as ul
import CFlowGraph as FG
import FordFulkerson as FF
########### MAIN  ######

N, data =  ul.load_connections("./W_data.dat")
myFG = FG.CFGraph(N)
myFG.addEdges(data)
#myG.print_Edges()

print "Max-Flow Min-Cut CFordFulkerson"

myFF = FF.CFordFulkerson(myFG)
myFF.compute(0,7)

print myFF.get_inCutV()