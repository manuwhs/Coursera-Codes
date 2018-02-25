#!/usr/bin/python
# -*- coding: utf-8 -*-

import math


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

