#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

# This funcion will get the possible nodes around a node we can swap it with.
# The way they are gonna be written is the same the layes are putted.
# Given: 14 16 44 15 38 29 43 50 39 49 48 32 17		Capa 1
#	 0  33 22 1  31 25 6  27 26 47 2  5  10 	Capa 2
#	 28 9  45 3  46 41 24 8  34 4  13 19 7 		Capa 3
#	 35 23 30 12 36 20 37 21 42 11 40 18		Capa 4
# Possibles will look like:
#	 [pos14][pos16 [pos44 [pos15 [pos38 [pos29 [pos43 [pos50 [pos39 [pos49 [pos48 [pos32 [pos17		Capa 1
#	 [pos0  [pos33 [pos22 [pos1  [pos31 [pos25 [pos6  [pos27 [pos26 [pos47 [pos2  [pos5  [pos10 	Capa 2
#	 [pos28 [pos9  [pos45 [pos3  [pos46 [pos41 [pos24 [pos8  [pos34 [pos4  [pos13 [pos19 [pos7 		Capa 3
#	 [pos35 [pos23 [pos30 [pos12 [pos36 [pos20 [pos37 [pos21 [pos42 [pos11 [pos40 [pos18		Capa 4

def get_possible(possible_points, capas, n):

# We get the posible points

	for k in range(0,len(capas)):	# For every node
	   for l in range (0,len(capas[k])):

	      pos_points = []

	      for i in range (0, n):		# For every layer we are gonna check
		for j in range (0,n):

# If we are at the extrem of the chart there will be some nodes that wont exist so we check it first
			if ( ((k + i - n/2) >= 0) and ((l + j - n/2) >= 0) ):	# Upper-left bound
				if ( ((k + i - n/2) < len(capas)) and ((l + j - n/2) < len(capas[k + i - n/2])) ):
					posib = capas[k + i - n/2][l + j - n/2]
					if (posib != capas[k][l]):
						pos_points.append(posib)
 #             print pos_points
	      possible_points[k][l] = pos_points


#---------------------------------------------------------------------------------------------------------------------------#
# Swaps the vertex of the solution.
# pos1 is the position of the origin node in the solution of the first vertex and pos2 that of the second

def swap_vertex (pos1, pos2, solution):

# The swap function:
#	a -> c -> f -> g -> i -> h -> e -> b -> d
#	       |                        |

# If we want to swap the vertez  c -> f and e -> b
# To make it feasible we have to join the starting and ending nodes so:
# We have to keep everything the same, break those bound and make:	c -> e and  f -> b 
# We should change the "f" with the and "b" so that one of the starting nodes points to
# the other starting point.   a -> c -> e -> g -> i -> h -> f -> b -> d
#				      | ^                   ^  |
#                                       |                   | 
#					---------------------
# The new configuration has the nodes:
#	|c -> e|,  e -> g,   h -> f    y  |f -> b|
# The old had:
#	|c -> f|,  f -> g,   h -> e    y  |e -> b|
# The canges in |  |  are the only ones we have to make

# Notice this has changed 4 vertex not 2, we have to change the direction of the middle edges:

# 			      a -> c -> e -> h -> i -> g -> f -> b -> d
#				      |      <--<--->-->      |

# Lets see if it doesnt matter changing any of the ways:
#	h -> e -> b -> d -> a -> c -> f -> g -> i
#	       |                    |

#			      h -> e -> c -> a -> d -> b -> f -> g -> i
#				      | ^    <---->    ^  |
#                                       |              | 
#					----------------
# THEY ARE THE SAME PATH (with diferent direction but doesnt affect the total length)
# We have to see which path is shorter

# Doing this, notice that the conection  f -> d is automaticly done  !!!
# So an 2-OTP is basicly changing the position of 2 nodes
# We dont need to check if any of the nodes is the last node in the solution list

# Case of 2 adyacent nodes 
#	a -> c -> f -> g -> i -> h -> e -> b -> d
#	             |         |

#	a -> c -> f -> i -> g -> h -> e -> b -> d
#	             | ^    ^  |
#                      |    | 
#		       ------
# We go from:
#	f -> g  and   i -> h     to      f -> i  and   g -> h
#	print pos1
#	print pos2

	if ( pos1 > pos2):
		aux = pos1
		pos1 = pos2
		pos2 = aux

	pos1 += 1

#	aux = solution[pos1]
#	solution[pos1] = solution[pos2]
#	solution[pos2] = aux
# Get the biggest:


	
# Shift optimization
	if ((pos2 - pos1) !=  0): 
		ax = 0
		if (pos2 - pos1 == 1):
			ax = 1
		for i in range (0, abs(pos2 - pos1)/2 + ax):
			aux = solution[pos2 - i]
			solution[pos2 - i ] =  solution[pos1 + i]
			solution[pos1 + i ] = aux

def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
def get_path (points, solution):
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, len(solution)-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

#----------------------------------------------------------------------------------------------------------------------#
# This funcion will realice a 2-opt and can be used to do any other function
#def 2OPT (node, path):
#------------------------------------------------------------------------------------------------------------------------#	
def compare (x,y):
	if (x[1]> y[1]) :
		return 1
	if ( x[1] == y[1]) :
		return 0
	if (x[1] < y[1]):
		return -1
#------------------------------------------------------------------------------------------------------------------------#
# We implement OPT and check with the "distance" nodes to see if there is a better direction.
# We break the link of the given point and next.
# To ensure feasibility we have to join the starting nodes of one vertex and their ending nodes
# otherwise it wont be feasible beacuese we will have 2 separate closed path.
# Notice that using the notation we have for the solution [n1 n2 n3 n4 n5...] it's imposible to get an unfeasible
# solution but it would create crrosing vertex and change and would change 4 vertex instead of 2 

# We have to:
#	1) Check for each one of the nodes the "distance" nodes wi
#	2) Check for every posible feasible combination between the posibilities
#	3) Pick the shortest one

def OPT2 (capas, layer, position, solution, points, possible_points):

	point1 = capas[layer][position]		# Valor del vertex a cambiar
	pos1 = solution.index (point1)		# Posicion del primer nodo del vertice en la solucion
	final = -1

	improve = 0

	for i in range (0, len (possible_points)):

		point2 = possible_points[i]
		pos2 = solution.index (point2)		# Posicion del primer nodo del vertice 2 en la solucion

# Get the ending nodes of the 2 vertex we are changing

		if (pos1 == len(solution) - 1):
			pos12 = 0
		else:
			pos12 = pos1 + 1

		if (pos2 == len(solution) - 1):
			pos22 = 0
		else:
			pos22 = pos2 + 1
		
		point12 = solution[pos12]
		point22 = solution[pos22]

		ini = length(points[point1], points[point12]) + length(points[point2], points[point22])
		fin = length(points[point1], points[point2]) + length(points[point12] , points[point22])

		improve_aux = ini - fin			# The new path fin has to be shorter 
		
		if (improve_aux > improve):
			improve = improve_aux
			final = i
# Notice we are taking the best improvement from all posible vertex break

# Now final has the best change value possible_points[final]. If final != -1, we make the swap
	# We get the position of the nodes in the solution to exchange them
#	print "Punto primero " + str(point1)

	if (final != -1):		# If there has been an improvement
		pos2 = solution.index (possible_points[final])
#		print "Mejora: " + str(improve) + " Nodos: " + str(point1) + " - " + str(possible_points[final]) + " Pos: " + str(pos1) + " - " + str(pos2)
		swap_vertex(pos1,pos2,solution)

#------------------------------------------------------------------------------------------------------------------------#
# layer: Number of layers						[IN]
# capas: The array of layers. capas = [layer1, layer2, layer3]		[OUT]
# ordered_nodes: Nodes ordered in X or Y				[IN]

def get_layers (layer, capas, ordered_nodes):

    nodeCount =len(ordered_nodes)
    if (layer % 2 == 1): 		# Layers must be even number
	layer += 1
    N_p_l = nodeCount/layer
    rest = nodeCount % N_p_l		# We will add this remaining 1 to each of the first rows

 
    print "Layer "+ str(layer) +  "  Nodos por Capa " + str(N_p_l) +" Rest " + str(rest)

    for i in range(0,rest):		# The ones with one more
	Y_ordered = ordered_nodes[i* (N_p_l +1): (i+1)* (N_p_l + 1)]
	Y_ordered.sort(cmp = compare)
	capas.append(Y_ordered)
   
    for i in range(0,layer-rest):
	Y_ordered = ordered_nodes[rest*(N_p_l + 1)+ i* N_p_l:rest*(N_p_l + 1)+ (i+1)* N_p_l]
	Y_ordered.sort(cmp = compare)
	capas.append(Y_ordered)

# Each node in the layer has its [X,Y,number], with the next code we eliminate the X and Y
    for i in range(0,layer):
	for j in range (0,len(capas[i])):
		capas[i][j] = capas[i][j][2]

#----------------------------------------------------------------------------------------------------------------------#

def connect_layers (capas, solution):
# capas: The array of layers. capas = [layer1, layer2, layer3]		[IN]
# solution: solution in order						[OUT]
    # We know that each layer has to be connected to another one by 2 nodes in order to close so
    # We connect the upper and buttom layer by the extrems and then joining the mid layer by the middle

# The number of layer must be an even number:
# 	2 layers  -> 0 middle
#	4 layers  -> 1 midlle
# 	6 layers  -> 2 middle
#	8 layers  -> 3 midlle

#                  	|----------------------------------------|	Upper line
#			|					 |	Goind Down right
#			|---------------|  	|----------------|			1     i-value
#					|	|			Middle
#			|---------------|  	|----------------|
#			|					 |
#			|---------------|  	|----------------|			2     i-value
#					|	|			Middle
#			|---------------|  	|----------------|
#			|					 |
#			|---------------|  	|----------------|			3     i-value
#					|	|			Middle
#			|---------------|  	|----------------|
#	Going up	|					 |
#			|----------------------------------------|	Downer line


# Notice for how the greedy solution was found that for a given node, if we want to use the OTP algorithm,
# mostlikely, the node closest to a node given will be around it.
# Given: 14 16 44 15 38 29 43 50 39 49 48 32 17		Capa 1
#	 0  33 22 1  31 25 6  27 26 47 2  5  10 	Capa 2
#	 28 9  45 3  46 41 24 8  34 4  13 19 7 		Capa 3
#	 35 23 30 12 36 20 37 21 42 11 40 18		Capa 4
# with Nodos por Capa: 12 y  Rest 3
#  Notice this ordering is just a 
# Mostlikely, the closest nodes will be in the same layer near the given node and the nodes near it of
# the surrounding layers. For example for node 4, the nodes that will be mostlikely closest will be:

#				 26 47 2  
#				 34    13  
#	 			 42 11 40 

# So it would make sense that if we choose at random the node 4 to remove it
# The other vertex we are gona break is one of those.
# We check for all those other posible nodes the improvement and choose the best
 

    pos_sol = 0		 # Posicion de la solucion
    layer = len(capas)	# Number of layers
    for i in range (0,len(capas[0])): 		#Upper line
 	solution[i] = capas[0][i]
	pos_sol += 1

    n_middle = (len(capas)-2 )/2
#    print "N_midle " + str(n_middle)
    for i in range (0, n_middle): 		# Going down
	layer1 = capas[1 + 2*i ]
	layer2 = capas[2 + 2*i ]
	rem1 = len(layer1) % 2
	rem2 = len(layer2) % 2

	for j in range (0, len(layer1)/2):
		solution[pos_sol] = layer1[len(layer1)-j -1]	# From last to half of next
								# In case of imparity we take the shortest
		pos_sol += 1

	for j in range (0, len(layer2)/2):
		solution[pos_sol] = layer2[len(layer2)/2 + rem2+ j]	# From half to last of next
		pos_sol += 1



    for i in range (0,len(capas[layer -1])): 			# Downer line
 	solution[pos_sol] = capas[layer - 1][len(capas[layer-1]) - i -1]
	pos_sol += 1

    for i in range (0, n_middle): 				# Going down
	layer1 = capas[(layer - 2) - 2*i]
	layer2 = capas[(layer - 3) - 2*i]
	for j in range (0, len(layer1)/2 + len(layer1) % 2):
		solution[pos_sol] = layer1[j]			# From first to half of next
		pos_sol += 1

	for j in range (0, len(layer2)/2 + len(layer2) % 2):
		solution[pos_sol] = layer2[len(layer2)/2 -1 + (len(layer2) % 2)- j]	# From half to first of next
		pos_sol += 1

#    print solution
#----------------------------------------------------------------------------------------------------------------------#

# def K-OPT
# K-OPT uses 2-OPT, we make a combination of breaking edges up until K and we look back
# to see where we had the best improvement. Cuestion is... if we are always taking the best
# improvement, de improvement always will grow as we break more bonds so...
# maybe we sould pick one at random from the posible ones... and as time grows, pick
# with more probability those with best single improvement (Temple simulado ? )



def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1]),i-1))
    # points = [[x0,y0,0][x1,y1,1][x2,y2,2][x3,y3,3]]
    # STEPS:
    # Build a trivial solution
    # We divide the nodes in layer of height and/or width 
    # We join all the nodes by X or Y axis of each layer and then we join the layers.
#-------------------------------------------------------------------------------------------------------------#

    capas = []				# Here we put the layers
    solution = [-1] * nodeCount


    X_ordered = points[:]
    X_ordered.sort()
    aux_solution = [-1] * nodeCount 
    aux_obj = 100000000000

    print "Nodos " + str(nodeCount)

    logic = int(math.sqrt(nodeCount))

    for i in range (0, 1):
   	    layer =  (i+1)*logic  # Layer ecuation
	    capas = []
	    get_layers (layer, capas, X_ordered)
	    connect_layers(capas, aux_solution)
#	    print str(capas[1][0]) +" = " + str(aux_solution[-1])

	    if (capas[1][0] == aux_solution[-1]):	 # If there was no error
	   	obj = get_path (points, aux_solution)
#		print obj
		if (obj < aux_obj):
			aux_obj = obj
			solution = aux_solution[:]	# Copy solution and the layers
			capas_fin = capas[:]

#--------------------------------------------------------------------------------------------------------------------------------------# Layers and greedy solution done

    possible_points = []
    possible_points = len(capas_fin) * [0] # Posible vertexes to swap to the given one
					  # (Will be the closest to the given vertex)         						  # Layers around we check
    for i in range (0, len(capas_fin)):
	possible_points[i] = len (capas_fin[i])*[0]



    layer = len(capas_fin)
    
    print "Capas Done: "
#    for i in range(0,layer):
#	print capas_fin[i]

    get_possible(possible_points, capas_fin, 13)

    print "Posibles Done: "

#    for i in range (len(possible_points)):
#	for j in range (len(capas_fin[i])):
#		print possible_points[i][j]

    print "La solucion es: " + str(aux_obj)
#    print solution
# Print the original solution !!!--------------------------------------------------------------------------------------


# For every node we try the 2-OPT
    for k in range (0,0):
	print "TIME ----------------------------------------------------------> " + str(k)

	for i in range(0,layer):
		print "Layer: " + str(i)
		for j in range (0,len(capas_fin[i])):
			OPT2 (capas_fin, i , j, solution, points, possible_points[i][j])	 # First and last
#			OPT2 (capas_fin, layer - 1 - i , len(capas_fin[layer - 1 - i]) - 1 - j, solution, points)
	print get_path (points, solution)





#	improvement = 0
#	for j in range (0, distance):
		


    # calculate the length of the tour
    obj = get_path (points, solution)

    f = open("./plot/in","w+")
    f.write(str(nodeCount)+ " ")
    for i in range (0, nodeCount):
	f.write(str(points[i][0])+" "+ str(points[i][1]) + " ")
    f.close()




    f = open("./plot/out","w+")
    for i in range (0, nodeCount):
	f.write(str(solution[i])+" ")
    f.close()

    # prepare the solution in the specified output format
    outputData = str(obj) + ' ' + str(0) + '\n'
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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

