#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

def get_possible(possible_points, capas, n):
# n: Number of points in every direction we are gonna look at
# We get the posible points
	n = 2*n + 1
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
# pos1 and pos2 are the position of the nodes in the solution.

def OTP2 (pos1, pos2, solution):

	if ( pos1 > pos2):
		aux = pos1
		pos1 = pos2
		pos2 = aux

	pos1 += 1

	if (pos2 - pos1 == 0):
		print "No hay cambio"
		return

	for i in range (0, abs(pos2 + 1 - pos1)/2):
		aux = solution[pos2 - i]
		solution[pos2 - i ] =  solution[pos1 + i]
		solution[pos1 + i ] = aux
#----------------------------------------------------------------------------------------------------------------------#
def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

#----------------------------------------------------------------------------------------------------------------------#
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
def check_idea(layer,pos,capas,points, n):
	distances = [0.0] * n
	num = [0] * n

	for i in range (0,n):
		possible_points = len(capas) * [0] # Posible vertexes to swap to the given one
		for j in range (0, len(capas)):
			possible_points[j] = len (capas[j])*[0]

		get_possible(possible_points, capas, 2*i + 3)
#		print possible_points[layer][pos]
		num[i] = len(possible_points[layer][pos])
		for j in range(0,num[i]):
#			print "Elegido " + str(capas[layer][pos])
#			print "Prox " + str(possible_points[layer][pos][j])
			distances[i] += length(points[capas[layer][pos]], points[possible_points[layer][pos][j]])
		
	for i in range(0,n-1):
		distances[n-1-i] -= distances[n-2-i]
		num[n-1-i] -= num[n-2-i]

	for i in range(0,n):
		distances[i] = distances[i]/num[i]
		print "Distancia de " + str(2*i + 3) +" Media: " + str(distances[i]) + "Objetos: " + str(num[i])
	
		

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

def best_swap (capas, layer, position,con,distances, solution, points, possible_points):

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

#		print distances[layer][position][i]
#		print length(points[point1], points[point2])
		aux = possible_points[layer][position].index(point12)
		print distances[layer][position][aux]
		print length(points[point1], points[point12])
		
		improve_aux = ini - fin			# The new path fin has to be shorter 
		
		if (improve_aux >= improve) and abs(pos1 - pos2) > 1:
			improve = improve_aux
			final = i

# Notice we are taking the best improvement from all posible vertex break

# Now final has the best change value possible_points[final]. If final != -1, we make the swap
	# We get the position of the nodes in the solution to exchange them
#	print "Punto primero " + str(point1)

	if (final != -1):		# If there has been an improvement
		pos2 = solution.index (possible_points[final])
#		print "Mejora: " + str(improve) + " Nodos: " + str(point1) + " - " + str(possible_points[final]) + " Pos: " + str(pos1) + " - " + str(pos2)
		OTP2(pos1,pos2,solution)

#------------------------------------------------------------------------------------------------------------------------#
def temple_simulado(capas, layer, position, solution, points, possible_points):
	
	print "go"


#------------------------------------------------------------------------------------------------------------------------#
# layer: Number of layers						[IN]
# capas: The array of layers. capas = [layer1, layer2, layer3]		[OUT]
# ordered_nodes: Nodes ordered in X or Y				[IN]

def get_layers (layer, capas, ordered_nodes):

    nodeCount = len(ordered_nodes)
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

def greedy (capas, solution):
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
	    greedy(capas, aux_solution)
#	    print str(capas[1][0]) +" = " + str(aux_solution[-1])

	    if (capas[1][0] == aux_solution[-1]):	 # If there was no error
	   	obj = get_path (points, aux_solution)
#		print obj
		if (obj < aux_obj):
			aux_obj = obj
			solution = aux_solution[:]	# Copy solution and the layers
			capas_fin = capas[:]

    print "Greedy Done "
#--------------------------------------------------------------------------------------------------------------------------------------# Layers and greedy solution done

    possible_points = []
    possible_points = len(capas_fin) * [0] # Posible vertexes to swap to the given one
					  # (Will be the closest to the given vertex)         						  # Layers around we check
    for i in range (0, len(capas_fin)):
	possible_points[i] = len (capas_fin[i])*[0]



    layer = len(capas_fin)
    
    print "Capas Done "
#    for i in range(0,layer):
#	print capas_fin[i]

    get_possible(possible_points, capas_fin, 3)

    print "Posibles Done "

# We now create for every node, the distance to each possible node.
#    print capas_fin
#    print " "
#    print possible_points

    distances = len(possible_points)*[-1] 

    for i in range (0, len(distances)):
	distances[i]= len(possible_points[i])*[-1] 

	for j in range (0, len(distances[i])):
		distances[i][j]= len(possible_points[i][j])*[-1] 

		for k in range (0, len(distances[i][j])):
			distances[i][j][k] = length(points[capas_fin[i][j]], points[possible_points[i][j][k]])

    for i in range (0, len(distances)):
	for j in range (0, len(distances[i])):
		print possible_points[i][j]
		print distances[i][j]

    print "Distances done"

#    for i in range (len(possible_points)):
#	for j in range (len(capas_fin[i])):
#		print possible_points[i][j]

    print "La solucion es: " + str(aux_obj)
#    print solution
# Print the original solution !!!--------------------------------------------------------------------------------------

    con = [-1] * nodeCount
    for i in range (0, nodeCount):
	con[i] = [-1, -1]

    for i in range(0, nodeCount):
	con[i][0] = i
	aux = solution.index (i)
	if (aux == nodeCount -1):
		con[i][1] = solution[0]
	else:
		con[i][1] = solution[aux+1]


# For every node we try the 2-OPT
    for k in range (0,5):
	print "TIME ----------------------------------------------------------> " + str(k)

	for i in range(0,layer):
#		print "Layer: " + str(i)
		for j in range (0,len(capas_fin[i])):
			best_swap (capas_fin, i , j,con, distances, solution, points, possible_points[i][j])	 # First and last
#			OPT2 (capas_fin, layer - 1 - i , len(capas_fin[layer - 1 - i]) - 1 - j, solution, points)
	print get_path (points, solution)

#    check_idea(0,0,capas_fin,points, 5)



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

