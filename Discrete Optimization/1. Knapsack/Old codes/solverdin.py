#!/usr/bin/python
# -*- coding: utf-8 -*-

def ite (weights, values,num_obj, cap ):
	if num_obj == 0:
		return 0
	elif weights[num_obj] <= cap :
		return max( ite (weights, values, num_obj-1, cap), values[num_obj] + ite (weights, values, num_obj-1, cap-weights[num_obj]) )
	else:
		return ite (weights, values, num_obj-1, cap)

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append([int(parts[1]),])

    items = len(values)

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = []

    table = capacity * [0]
    for num in range(0, capacity):
	table[num] = items * [0]
    


    for num in range(1, items):
	for cap in range(1, capacity-1):
		table[cap][num] = ite(weights, values,num,cap)
		print " Tenemos " + str(num) +" "+str(cap) + " = " + str(table[cap][num])
    print table

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))
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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

