#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(n):
    # Modify this code to run your puzzle solving algorithm
    # We are gonna use the Siamese method
    sol = [-1] * n
    for i in range (0, n):
	sol[i] = [0] * n
    count = 1
    X = n/2
    Y = 0

    sol[Y][X] = 1
    fail = 1 
    while (count  < n*n):
	fail = 1
	while (fail == 1 ):
		X_aux = X
		Y_aux = Y
		if (X + 1 > n - 1):
			X = 0
		else:
			X = X + 1 

		if (Y - 1 < 0):
			Y = n - 1
		else:
			Y = Y - 1

		if (sol[Y][X] == 0):
			sol[Y][X] = count + 1
			fail = 0
			count += 1
		else:
			X = X_aux
			Y = Y_aux

			if (Y + 1 > n -1):
				Y = 0
			else:
				Y = Y +1

			if (sol[Y][X] == 0):
				sol[Y][X] = count + 1
				fail = 0
				count += 1
	

    # Lets swap it
    for i in range (0, n):
	for j in range (0, n/2):
		aux = sol[j][i]
		sol[j][i] =  sol[n -1-j][i]
		sol[ n - 1-j][i] = aux

    outputData = str(n) + '\n'

    for i in range(0,n):
            outputData += ' '.join(map(str, sol[i]))
    	    outputData += '\n'
    return outputData




# checks if an assignment is feasible
# because sol is an array (not a matrix), checks are more cryptic
import math
def checkIt(sol):
    n = int(math.sqrt(len(sol)))
    m = n*(n*n+1)/2
    
    #for i in range(0,n):
    #    print sol[i*n:(i+1)*n]
    
    items = set(sol)
    if len(items) != len(sol):
        #print len(items),len(sol) 
        return False
    
    for i in range(0,n):
        #print 'row',i,sol[i*n:(i+1)*n]
        if sum(sol[i*n:(i+1)*n]) != m:
            return False
        #print 'column',i,sol[i:len(sol):n]
        if sum(sol[i:len(sol):n]) != m:
            return False
        if i < n-1:
            if sol[i*n+i] > sol[(i+1)*n+(i+1)]:
                return False 
    
    #print 'diag 1',i,[sol[i*n+i] for i in range(0,n)]
    if sum([sol[i*n+i] for i in range(0,n)]) != m:
        return False
    #print 'diag 2',i,[sol[i*n+(n-i-1)] for i in range(0,n)]
    if sum([sol[i*n+(n-i-1)] for i in range(0,n)]) != m:
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
        print('This test requires an instance size.  Please select the size of problem to solve. (i.e. python magicSquareSolver.py 3)')

