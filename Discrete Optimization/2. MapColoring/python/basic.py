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

#-----------------------------------------------------------------------------------------------------------------------
# This function will color a node with the lowest value posible from the available values,
# if it needs more colors it will increase them.

def color_node (nodes, n_colors ,node_to_color):
	aux_colors = []		# Auxiliary list of invalid colours for a node

# We check all the colors of the conected nodes and save them in aux_colors.
# The way we are doind it, its imposible that we have 2 conections with the same color

	if (nodes[node_to_color].n_edges == 0):
		print "Jajajaja"

	for i in range (0,nodes[node_to_color].n_edges):

		conected_color_node = nodes[nodes[node_to_color].edges[i]].color

		if ((conected_color_node != -1)and(aux_colors.count(conected_color_node)== 0)):
			aux_colors.append(conected_color_node)
#			print "Color " + str (conected_color_node) + " eliminado para nodo " + str( node_to_color)

# Now we have in aux_colors all the colors that that node cannot have so we choose the lowest it can have
# If it cannot have any of the colors that we have already we add a color and give it to the node

	if (len(aux_colors) == 0 ):
		nodes[node_to_color].color = 0

	elif (len(aux_colors) == n_colors[0] ):
#		print "Nuevo color ( " + str(n_colors[0]) + " ) para nodo " + str(node_to_color)
		nodes[node_to_color].color = n_colors[0]
		n_colors[0] += 1

	else:
		aux_colors.sort()
#		print aux_colors
#		print "Color no añadido"

		for j in range (0, len(aux_colors)):

			if (aux_colors[j] != j ):
				nodes[node_to_color].color = j
				break
# It may happen that we have knocked out a set of colors from 0 to m, so the method shown up doesnt work
# Thats why we add this case here
			if (j == len(aux_colors) -1):
				nodes[node_to_color].color = j + 1
			
#	print "Node " + str (node_to_color) + " colored with color " + str(nodes[node_to_color].color)
	return 1	# Means job done

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
    colored_nodes = []	# Number of colored nodes
    n_colors = [0]

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

 
# Very simple aproximation:	
	# We color one node and their conected nodes with diferent colours, then we go thrpugh all 
	# the non-coloured nodes and check the colours of their adjacent nodes and colour them
	# with the lowest color number so far ("to avoid symetry")
	# This way there will be no need to check feasibility, because if we keep adding colours
	# it will always be feasible. We will start from to node 0 to the end

# We color first node and sorrounding nodes

# While we havent coloured all nodes, we look through the ones that has been coloured, look for their conection
# and colour them checking those conection nodes. If we can colour it with more than one color we choose the lowest
   

    nodes[0].color = 0

    n_colors[0] += 1
    colored_nodes.append(0)
    
    for i in range(0, nodes[0].n_edges):
	nodes[nodes[0].edges[i]].color = i + 1
#	print "Nuevo color ( " + str(n_colors[0]) + " ) para nodo " + str(nodes[0].edges[i])
	n_colors[0] += 1 
#    print " "

    for i in range (0,  nodeCount):
	if (nodes[i].color == -1 ):	# If the node havent been colored yet
		color_node (nodes, n_colors ,i)

# Chequing


    for i in range (0,  nodeCount):
	for j in range (0, len(nodes[i].edges)):
		if (nodes[i].color == nodes[nodes[i].edges[j]].color):
			print "Error nodos "+ str(i) + " - " +str(nodes[i].edges[j])


# Shud be done already

    solution = [-9]*nodeCount

    for i in range (0, nodeCount):

	solution[i] = nodes[i].color

    # prepare the solution in the specified output format
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

