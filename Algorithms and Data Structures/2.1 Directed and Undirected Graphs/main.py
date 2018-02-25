# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import util as ul
import CDiGraph as DG
import CPath as Path
import CConnected as CC
import CDeepFirstOrder as CDFO
import KosarajuSharirSCC as KSSCC

########### MAIN  ######

N, data =  ul.load_connections("./UF_data.dat")
myG = DG.CGraph(N, directed = False)
myG.addEdges(data)
#myG.print_Edges()

# FIND PATHS FROM A NODE
######### Do a Deep First Search
print "Deep Search First"
myPath = Path.CPath(myG, 1)

myPath.DeepFirstSearch()
print myPath.marked
print myPath.pathTo(5)

######### Do a Deep First Search
print "Breadth Search First"
myPath.BreadthFirstSearch()
print myPath.marked
print myPath.pathTo(5)


### CONNECTED Undigraph
N, data =  ul.load_connections("./UF_data.dat")
myG = DG.CGraph(N, directed = False)
myG.addEdges(data)
print "Connected in a Undirected Graph"
myC = CC.CConnected(myG)
myC.DeepFirstSearch()
print myC.id

### Order in DAG
print "Order in a DAG"
N, data =  ul.load_connections("./DAG.dat")
myG = DG.CGraph(N, directed = True)
myG.addEdges(data)

myCDFO = CDFO.CDFO(myG)
myCDFO.DeepFirstOrder()
print myCDFO.getOrder()

### Strongly Connected
print "Strongly Connected in Directed Graph"
N, data =  ul.load_connections("./SC.dat")
myG = DG.CGraph(N, directed = True)
myG.addEdges(data)

myKSSCC = KSSCC.KSCC(myG)
myKSSCC.DeepFirstSearch()
#print myKSSCC.marked
print myKSSCC.id

