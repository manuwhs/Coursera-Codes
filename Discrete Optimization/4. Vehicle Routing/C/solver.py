
import os
import subprocess
def solveIt(inputData):
    # parse the input
    lines = inputData.split('\n')

    parts = lines[0].split()
    customerCount = int(parts[0])
    vehicleCount = int(parts[1])
    vehicleCapacity = int(parts[2])
    depotIndex = 0

    customers = []
    for i in range(1, customerCount+1):
        line = lines[i]
        parts = line.split()
        customers.append((int(parts[0]), float(parts[1]),float(parts[2])))
    ### Writes the inputData to a temporary file
    tmpFileName = 'tmp.data'
    tmpFile = open(tmpFileName,'w')
    tmpFile.write(inputData)
    tmpFile.close()

#--------------------------------------------------------------------------------------------------
    ### Call your program, e.g. Test, with the file name as argument(s)
    process = subprocess.call(['./vrp',"20"])
    print "Programa terminado"

    f = open("out","r+")

    data_aux = f.readline()
    data_aux = data_aux.split(" ")

    outputData = str (data_aux[0]) + " "  + str(0) + str("\n")
    
    for i  in range (0, (int)(data_aux[1])):
	solution_aux = f.readline()
    	solution_aux = solution_aux.split(" ")
	solution = [0] * (len(solution_aux) -1)
	for j in range (0, len(solution_aux)-1):
		solution[j] = (int)(solution_aux[j])
    	outputData += ' '.join(map(str, solution)) + str("\n")
    f.close()
    return outputData



# Here we check if a filename is given, we call it, and we call the function
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

