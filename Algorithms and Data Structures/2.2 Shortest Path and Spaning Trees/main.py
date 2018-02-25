# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import util as ul
import CWDiGraph as DG
import DijkstraSP as Dijk
import DAGSP as DAGSP
import BellmanFord as BF
########### MAIN  ######

N, data =  ul.load_connections("./W_data.dat")
myG = DG.CWGraph(N, directed = False)
myG.addEdges(data)
#myG.print_Edges()


### Krustal KMST for computation
#myKMST = KMST.CKrustalMST(myG)
#MST = myKMST.compute()
#print MST
## TODO Prism
## TODO Klustering


# Shortest Path Algorithm
# Dijkstra fails to do "./W2_data3.dat" because it does not recheck
# nodes that have already been processed.
# If we removed this constraint, we are fine.

print "Shortest Path using Dijkstra"
N, data =  ul.load_connections("./W2_data3.dat")
myG = DG.CWGraph(N, directed = True)
myG.addEdges(data)

myDijk = Dijk.CKDijkstraSP(myG)
shit = myDijk.computeSP(0)
print shit
#print len(myG.G[0])

N, data =  ul.load_connections("./W2_data3.dat")
myG = DG.CWGraph(N, directed = True)
myG.addEdges(data)

## SP algorithm for DAGs
print "Shortest Path for DAGs"
myDAGSP = DAGSP.CDAGSP(myG)
shit = myDAGSP.computeSP(0)
print shit
print len(myG.G[0])

## SP algorithm using BellmanFord
print "Shortest Path using BellmanFord"
myBF = BF.CBellmanFord(myG)
shit = myBF.computeSP(0)
print shit
print len(myG.G[0])

## Negative Cycle Detection BellmanFord
print "Negative Cycle Detection BellmanFord"
N, data =  ul.load_connections("./W3_data.dat")
myG = DG.CWGraph(N, directed = True)
myG.addEdges(data)

myBF = BF.CBellmanFord(myG)
shit = myBF.computeSP(0)
print shit
print len(myG.G[0])



