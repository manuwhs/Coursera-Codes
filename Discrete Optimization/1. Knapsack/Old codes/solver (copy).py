#!/usr/bin/python
# -*- coding: utf-8 -*-

#    params = [weights values nodes items best major_node depth]

class node:
	def __init__ (self, branch, value, room, estimate, depth):
		self.branch = branch
		self.value = value
		self.room = room
		self.estimate = estimate
		self.depth = depth

# Creates the next two nodes from a node and adds it to the end of the nodes list
def split_node (n,pa):

	node_1 =  node(n.branch + [1],n.value + pa[1][n.depth],n.room - pa[0][n.depth],n.estimate, n.depth + 1)
	node_0 =  node(n.branch + [0],n.value, n.room ,n.estimate -  pa[1][n.depth], n.depth + 1)
	pa[2].append([node_1, node_0])



def checknode (n,pa):
# We have to stop a branch if its estimation and value are lower than the best best value so far
# if it exeds the room
	print n.branch
#	print n.room
	if (((n.estimate <= pa[4])and(n.value <= pa[4]))or n.room < 0): 
#		print ("Room")
# Si esta es la ultima rama que vamos a ver. Es la ultima si la desechamos y tiene todo 0's. Indicamos que de acabo
		if (n.branch.count(0) == n.depth):
			return 2

# Si esta es la segunda rama del nodo superior habra que eliminar el nodo superior y todos los anteriores
# hasta toparnos con un 1, en cuyo caso se probara el 0 de esa posibilidad
		if(n.branch[n.depth-1] == 0):
#			print "Rama 0 eliminada"
			elim = n.branch
			i = 1
			while (elim[-i]==0):
				del pa[2][-1]
				i = 1+i
			return 0
#		print "Profundidad: "+ str(n.depth)
#		print "Estimacion demasiado baja"
		return 0

# Now we check if we have room for the next object, if not, we specify this one as the best so far
# because due to the 

# We chech if we got to the end of the tree with a better feasible solution or 
# Comprobamos si al añadir el siguiente se nos va por lo que acabamos la 
	elif (n.depth == pa[3]):
		if (n.value > pa[4]):
			print "New Best:" + str (n.value)
			pa[4] = n.value
			pa[5] = n.branch
			elim = n.branch
			i = 1
			del pa[2][-1]
			while (elim[-i -1]==0):
				del pa[2][-1]
				i = 1+i
			return 0
		else:
			return 1
	else:

		split_node (n,pa)
		return 1

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    nodes = []
    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    items = len(values)

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    estimate = 0
    estimate2 = 0
    weight = 0
    nodos = []
    best = 0
    depth = 1
    finish = 1
    density = []
    taken = items * [0]


    for i in range(0, items):
	aux = float(values[i]) / weights[i]
        density.append([aux,i])
    density.sort() 
    density.reverse()

    solved = 0
    i = 0
    while solved != 1:
   	pos = density[i][1]
        if weight + weights[pos] <= capacity:
            estimate += values[pos]
            weight += weights[pos]
            i = i+1

        else: 
            estimate += int (density[i][0]*(capacity - weight))
            solved = 1
    estimate = int(estimate * 1)
    print "Estimation: " + str(estimate)
# Estimation -----------------------------------------------------
    for i in range(0,items):
		estimate2 += values[i]
    print "Todos: " + str(estimate2)

#    estimate = estimate2/items + estimate

    print "Usado: " + str(estimate)

    estimate = estimate2

# Now we have our relaxation value

#    weights.sort()
#    weights.reverse()
    node_X1 = node([1],values[0],capacity - weights[0],estimate,1)
    node_X0 = node([0],0,capacity, estimate-values[0],1)

    nodes.append([node_X1, node_X0 ])
    params = [weights, values, nodes, items, best, taken, depth]

    while (finish != 2):
	if (finish == 1):
      	   finish = checknode (params[2][-1][0], params)
	if (finish == 0):
           finish = checknode (params[2][-1][1], params)

    taken = params[5]
    value = params[4]

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData

# Creates the next two nodes from a node and adds it to the end of the nodes list


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

