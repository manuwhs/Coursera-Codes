#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(n):
    # We are gonna use a constructive heurisic algorith to get the points beaches !!!
    sol = n * [-2]
    for i in range (0, n/2 + n%2):
    	sol[2*i] = i
    for i in range (0, n/2):
    	sol[2*i+1] = n - i -1

    # start a trivial depth first search for a solution

    # prepare the solution in the specified output format
    # if no solution is found, put 0s
    outputData = str(n) + '\n'

    outputData += ' '.join(map(str, sol))+'\n'
 
    return outputData




# checks if an assignment is feasible
def checkIt(sol):
    n = len(sol)
    
    items = set(sol)
    if len(items) != n:
        return False
    
    deltas = set([abs(sol[i]-sol[i+1]) for i in range(0,n-1)])
    if len(deltas) != n-1:
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
        print('This test requires an instance size.  Please select the size of problem to solve. (i.e. python allIntervalSeriesSolver.py 5)')

