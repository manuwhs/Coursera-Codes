#!/usr/bin/python
# -*- coding: utf-8 -*-

class node:
	def __init__ (self,number):
		self.number = number
		self.n_edges = 0
		self.edges = []
		self.color = -1  # Indicates there is no color associtated
	def color (self, color):
		self.color = color
	def add_edge (self, edge):
		self.n_edges += 1
		self.edges.append(edge)
#		print "Node: " + str(self.number) + " added node " + str(edge)
	def set_colors (self, num_colors):
		self.posible = range (0, num_colors -1)


#----------------------------------------------------------------------------------------------------------------------- #
# This funcion will be used to order de nodes in increasion number of branches

def compare (x,y):
	if (x.n_edges > y.n_edges ) :
		return 1
	if ( x.n_edges == y.n_edges) :
		return 0
	if (x.n_edges < y.n_edges):
		return -1

#----------------------------------------------------------------------------------------------------------------------- #
# This function will check feasibility of all unresolved nodes and prune them
# If there is any pruning we put in a queue the pruned nodes to check if we can
# It prunes the search-space of all nodes conected to a node we have just colored and checks if it
# feasible by looking at the number of posible colors.
# If its not feasible we add a new posible color and start over

def pruner_feas (nodes, color, aux_conection, nodes_queue,order):

	for i in range (0, len(aux_conection)):

		conected_node = nodes[order[aux_conection[i]]]
		if (conected_node.posible.count(color) == 1 ):
			conected_node.posible.remove(color)
			
		if (len (conected_node.posible)== 1):
			nodes_queue.insert(0, conected_node.number) # We add it to the queue por pruning
			return 0

		if (len (conected_node.posible)== 0):
			return -1
	return 0
#----------------------------------------------------------------------------------------------------------------------- #
# We color the node "node_to_color", and save it in the "colored" nodes and we remove it from the rest of the nodes
# and the corresponding conections. Then we prune it and check feasibility but to do so we have to know the removed
# node conection, that why we create de "aux_conection" to keep them.
 	
def color_node (nodes, node_to_color,aux_conections ,colored, nodes_queue, order):
	aux_conection = []
	color = nodes[order[node_to_color]].posible[0] 	# We color with the minimum color posible
	colored.append([node_to_color, color])		# We store the saved value

	for i in range(0, nodes[order[node_to_color]].n_edges):	# For every conection the node had

		conected_node = nodes[order[node_to_color]].edges[i]
		aux_conection.append(conected_node)			# We keep the conection in an aux var
		nodes[order[conected_node]].edges.remove (node_to_color)	# We remove the conection from the node
		nodes[order[conected_node]].n_edges -= 1

	del nodes[order[node_to_color]] 				# We eliminate the node

	order[node_to_color] = -1			# We erase the node from the order list
							# and decrease the ones after		
	for i in range (node_to_color,len(order)):
		order[i] -= 1

	if (pruner_feas (nodes, color, aux_conection, nodes_queue, order)== -1):		# Prune the search-space due to the
		return -1								# colored node
	return 0


#----------------------------------------------------------------------------------------------------------------------- #
# This function will make a decision of a which node to color and it will be colored
# with the minimum color number posible.
# It will select the node with less conections posible

def decision_maker (nodes, nodes_queue):
	ordered_list = nodes[:]
	ordered_list.sort (cmp = compare)
#	print "Decision is node " + str (ordered_list[0].number)
	nodes_queue.insert(0,ordered_list[len(ordered_list)-1].number)

#------------------------------------------------------------------------------------------------------------

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])
    edgeCount = int(firstLine[1])

    edges = []		# Variable to store all edges
    nodes = []		# Here we store all node objects
    colored= []		# When we color a node we will prun the colors of the other nodes and remove it
			# from the search tree so that we dont go over it again.
			# Here we will put pairs [node color] of the colored nodes.

    n_colors = [0]
    resolved_nodes = []	# When we color a node we take it off "nodes" and put it here
    nodes_queue = []	# When pruning the search-space of nodes because we colored one
			# it may happen that we can color a node because it has no more colors left
			# so we color it and its nodes will have to be prunned

    order = [] 	# As we eliminate nodes from "nodes" we wont be able to directly locate a node
			# in the aray "nodes",we would have to check the parameter "number" of all of them
			# To solve this we have this variable which position [i] tells us where the node
			# "i" is placed in "nodes". Removed nodes will have value -1 in this array

    aux_conections = []

    for i in range(1, edgeCount + 1):		
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

# First of all we create all node instances

    for i in range(0,nodeCount):
        node_aux = node(i)
	nodes.append(node_aux)

# Now we add to the branches to the nodes

    for i in range (0,edgeCount):
	nodes[edges[i][0]].add_edge(edges[i][1])
	nodes[edges[i][1]].add_edge(edges[i][0])

    nodes_copy = nodes[:]	# We copy the nodes so that if the initial number of nodes
				# is not fasible we can start over
    nodes_aux = nodes[:]

# Now we check for the minimum number of colors it can have, which is the maximum number
# of conections a node has.

    nodes_aux.sort (cmp = compare)
    n_colors[0] = nodes_aux[nodeCount-1].n_edges
    nodes_aux = []				# Eliminate it so that it doesnt take up space


# We start by tring to fill the nodes with the minimum number posible.
# When we find an unfeasible solution we add up a new color and start over
# ( Posible changes: When an unfeasibily happens go back in a decision tree and do something else
#		     When we see we need more colors we just add up that new color to the list 
#		     of colors the uncolored nodes can have )


    n_colors[0] -= 1	# We do that so we can use the loop for the first value as well
    add_color = 1
    order = range(0,nodeCount)
    while (len(colored) != nodeCount):		# While all nodes havent been colored
	if (add_color == 1):			# If it wasnt feasible to do it with the last number of colors
		colored = []
		nodes = nodes_copy[:]
		queue = []
		n_colors[0] += 1
#		print " Numero de colores: " + str(n_colors[0])
		for i in range (0, nodeCount):	# Set the search space
			nodes[i].set_colors(n_colors[0])
		add_color = 0
		
	if (len(nodes_queue) == 0 ):		# If there is no more nodes to prune or color
		decision_maker(nodes, nodes_queue)		# We start the decion maker which will select a node to

#	print "Cola:"
#	print nodes_queue
	feasible = color_node (nodes,nodes_queue[-1],aux_conections, colored, nodes_queue, order); # We color the node, which will propagate
#	print "Node colored " + str(nodes_queue[-1])
	if (feasible == -1):
#		print " No ha sido posible hacerlo con " + str (n_colors[0]) +" colores"
		add_color = 1
	del nodes_queue[-1]			# Delete the node from the queue coz its been colored

	

# Chequing

    colored.sort()
    nodes = nodes_copy
    
    for i in range (0,  nodeCount):
	nodes[i].color = colored[i][1]
    for i in range (0,  nodeCount):
	for j in range (0, len(nodes[i].edges)):
		if (nodes[i].color == nodes[nodes[i].edges[j]].color):
			print "Error nodos "+ str(i) + " - " +str(nodes[i].edges[j])

# Shud be done already

    solution = [-9]*nodeCount

    for i in range (0, nodeCount):
	solution[colored[i][0]] = colored[i][1]

    # prepare the solution in the specified output format
    
    n_colors[0] = max (solution) + 1
    outputData = str(n_colors[0]) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))

    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'






#    while (num_resolved != nodeCount):
#
#    	for i in range (0, nodes[root_node[-1]].n_edges):
#		print "HOla " + str(i)
#		if (nodes[root_node[-1]].color == -1 ):	# If the node havent been colored yet
#			print "Hey"
#			color_node (nodes, n_colors ,root_node[-1], root_node)
#			root_node[-1] = []					# Remove the explored node
#			num_resolved += 1
			


