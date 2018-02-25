#!/usr/bin/python
# -*- coding: utf-8 -*-


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
        weights.append(int(parts[1]))

    items = len(values)

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    density = []
    taken = items * [0]


    last = 0
    removed = []

    for i in range(0, items):
	aux = float(values[i]) / weights[i]
        density.append([aux,i])
    density.sort() 
    density.reverse()
    print density

    solved = 0
    i = 0
    while (solved != 1):
        pos = density[i][1]
        if capacity == weight:
            solved = 1
        if i == items:
            solved = 1
        print str(pos) + " - " + str (weight+weights[pos])
        if weight + weights[pos] <= capacity:
            taken[pos] = 1
            print "Dato: "+ str(pos) +" introducido  \n"
            value += values[pos]
            weight += weights[pos]
            last = i

        else: # Vemos si quitamos alguno de los anteriores
            for j in range(0,i)
		aux = density[j][1]
                gain = values[density[last][1]] - density[i][0]*(capacity -(weight - weights[density[last][1]]))

            if (taken.count(1) >= 1):
                if (gain > 0 ):
                     print "Dato: "+ density[last][1] +" removido \n"
                     print "Dato: "+ str(pos) +" introducido  \n"
                     taken[last] = 0
		     taken[i] = 1
                     value = value - values[last] + values [pos]
                     weight = weight - weights[last] + weights[pos]
                     last = i
                else:
                     solved = 1
                     print "joke"
        i = i+1
# Now we have our relaxation value


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

