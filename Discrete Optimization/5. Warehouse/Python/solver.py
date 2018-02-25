#!/usr/bin/python
# -*- coding: utf-8 -*-

# This will get the new of the closed factories

def get_Costs_and_fill (cap_left, warehouses, wa_best, wa_cost, op_wa,customerSizes, wa_co, taken_co, order):
# Compute the cost of all not taken warehouses
    warehouseCount = len (warehouses)
    customerCount = len (wa_best[0])
    for i in range (0, warehouseCount):
	if (op_wa[i] == 0):		# Compute only if warehouse close
		wa_cost[i][0] = warehouses[i][1]
		cap_left[i] = (int) (warehouses[i][0])

		for j in range (0, customerCount):
			if (taken_co[wa_best[i][j][1]] == 0):	# If the object isnt already taken

				if (customerSizes[wa_best[i][j][1]] <= cap_left[i]):
					cap_left[i] -= customerSizes[wa_best[i][j][1]]
					wa_cost[i][0] +=  wa_best[i][j][0]
					wa_co[i].append(wa_best[i][j][1])
				else:
					break

    for i in range (0, warehouseCount):
	if (len(wa_co[i]) != 0):
		wa_cost[i][0] = wa_cost[i][0] / len(wa_co[i])
    wa_cost.sort()
    print wa_cost




def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    parts = lines[0].split()
    warehouseCount = int(parts[0])
    customerCount = int(parts[1])

    warehouses = []
    for i in range(1, warehouseCount+1):
        line = lines[i]
        parts = line.split()
        warehouses.append((int(parts[0]), float(parts[1])))

# warehouse[i][0] -> Capacity of warehouse [i]
# warehouse[i][1] -> Cost of warehouse [i]
# costumerSizes[i] -> Size of costumer [i]
# costumerCosts[i] -> Array with the costs to each warehouse -> costumerCosts[i][j] = cost of costumer i to warehouse j

    customerSizes = []
    customerCosts = []

    lineIndex = warehouseCount+1
    for i in range(0, customerCount):
        customerSize = int(lines[lineIndex+2*i])
        customerCost = map(float, lines[lineIndex+2*i+1].split())
        customerSizes.append(customerSize)
        customerCosts.append(customerCost)

 #   for i in range(0, customerCount):
 #  	 print customerCosts[i]
 #   print " "


# Cap_left is the capacity left for each warehouse.
    cap_left = [0] * warehouseCount
    for i in range (0, warehouseCount):
	cap_left[i] = (int) (warehouses[i][0])

# For every warehouse we create the list of most suitable costumers:
#[[100.1, 0], [100.4, 1], [200.1, 3], [200.7, 2]]
#[[100.8, 2], [200.11, 3], [200.2, 0], [200.5, 1]]
#[[100.12, 3], [2000.3, 0], [2000.6, 1], [2000.9, 2]]

# VARIABLES INICIATION:

    wa_best = [0] * warehouseCount
    order = [-1]*warehouseCount
    taken = 0

    for i in range(0, warehouseCount):
	wa_best[i] = customerCount * [-1]
	order[i] = customerCount * [-1]

    for i in range (0, warehouseCount):
	for j in range (0, customerCount):
		wa_best[i][j] = [customerCosts[j][i], j]

	wa_best[i].sort()
#	print wa_best[i]

#	print order[i]


# wa_cost [i] = [cost of warehouse "i",i] if its filled with the best remaining objects.
# and we divide it by the number of costumers it has.

# op_wa[i] --> If [i] is 0, warehouse i is closed, if i is 1, its opened

    wa_cost = [0] * warehouseCount

    op_wa = [0] * warehouseCount

    for i in range(0,warehouseCount):
	wa_cost[i] = [-1.0, i]


    wa_co = []
    for i in range (0, warehouseCount):
	wa_co.append([])


    taken = 0
    taken_co = [0] * customerCount # If "1" it means the object is already taken

    get_Costs_and_fill (cap_left, warehouses, wa_best, wa_cost, op_wa, customerSizes, wa_co, taken_co, order)

#    print wa_cost
#    print wa_co


# For each costumer, we create a list with the top "X" warehouses that are the cheapest for that costumer.
# This will be used for the "Local Search + Simulated Anneling + Tabu Search" algorithm.


# Greedy:
# Choose a costumer and open the first "Y" warehouses closer to it.
# Then look thourgh all costumers till finding  some with that warehouse among their top X and
# add it to a "list" for that warehouse. Those will be the possible costumers to add to the warehouse.
# Add the costumers to the warehouse in decreasing order of value until the warehouse is full.
# Keep picking costumers until this is done.

# To speed up things, we will create an order[i][j], with the order in wich the costumers are put in every warehouse
    open_wa = []
    while (taken < customerCount):

        for i in range (0, warehouseCount):
		pos = wa_cost[i][1]	# number of the warehouse we are opening
		if (op_wa[pos] == 0):
			op_wa[pos] = 1		# Open the warehouse
			break
	print "Warehouse elegida: "+ str(pos)
	open_wa.append([pos, cap_left[pos], wa_cost[i][0], wa_co[pos]])
	print open_wa

	for i in range(0, len(open_wa[-1][3])):
		print open_wa[-1][3][i]
		taken_co[open_wa[-1][3][i]] = 1		# Say we took that costumer
	
	for i in range (0,warehouseCount):
		wa_co[i] = []
		wa_cost[i][1] = i
							# Recompute Costs and capacities

	taken += len(open_wa[-1][3])	# The ones we are gonna delete

# Now we redoo the order because we have deleted one item


        get_Costs_and_fill (cap_left, warehouses, wa_best, wa_cost, op_wa, customerSizes, wa_co, taken_co, order)
#	print wa_cost
#	print wa_co
	

	

    solution = [-1] * customerCount
    obj = 0.0
    obj2 = 0.0

    for i in range (0, len(open_wa)):
	obj += open_wa[i][2] * len(open_wa[i][3])
	for j in range(0, len(open_wa[i][3])):
		solution[open_wa[i][3][j]] = open_wa[i][0]

    for i in range (0, len(open_wa)):
	obj2 += warehouses[open_wa[i][0]][1] 
	for j in range(0, len(open_wa[i][3])):
		obj2 += customerCosts[open_wa[i][3][j]][open_wa[i][0]]
    print obj2

# There will be a list op_wa [warehouseCount] with all the open and close warehouses
# We will have an array called:		open_wa[len(op_wa)]
# Every opened warehouse will be there indicating:	[num_Wa, room, total_cost, [list of costumers] ]



# Our algorithm will focus on the number of warehouse we have to open.

# Time for our local search algorithm. We can so several things, we have to make sure the neighbourhood is connected,
# This involves changing costumers between warehouses and oppening and closing others

#	Exchange costumers among warehouses
#	For a given costumer check if there is warehouse which will suit it better

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
        print 'Solving:', fileLocation
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/wl_16_1)'

