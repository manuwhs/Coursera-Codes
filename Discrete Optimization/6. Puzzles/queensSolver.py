#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(n):
    # We are gonna use the constructive heuristic:
    
    # start a trivial depth first search for a solution
    sol = n * [0]
    for i in range (0,n/2 + 1):
	sol[2*i] = i
    for i in range (0,n/2):
    	sol[2*i + 1] = n/2 + i +1
    # prepare the solution in the specified output format
    # if no solution is found, put 0s
    outputData = str(n) + '\n'
    outputData += ' '.join(map(str, sol))+'\n'
        
    return outputData


# this is a depth first search of all assignments


# checks if an assignment is feasible
def checkIt(sol):
    n = len(sol)
    for i in range(0,n):
        for j in range(i+1,n):
            if sol[i] == sol[j] or \
               sol[i] == sol[j] + (j-i) or \
               sol[i] == sol[j] - (j-i):
                return False
    return True


import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1].strip())
        except:
            print sys.argv[1].strip(), 'is not an integer'
        print 'Solving Size:', n
        print(solveIt(n))

    else:
        print('This test requires an instance size.  Please select the size of problem to solve. (i.e. python queensSolver.py 8)')

