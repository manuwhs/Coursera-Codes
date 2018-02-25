
import os
import subprocess
def solveIt(inputData):

    ### Writes the inputData to a temporary file
    tmpFileName = 'tmp.data'
    outFile = 'out'
    tmpFile = open(tmpFileName,'w')
    tmpFile.write(inputData)
    tmpFile.close()

#--------------------------------------------------------------------------------------------------

    ### Call your program, e.g. Test, with the file name as argument(s)
    process = subprocess.call(['java','Coloring',tmpFileName,outFile])
    print "Programa terminado"
#--------------------------------------------------------------------------------------------------

    lines = inputData.split('\n')
    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])

    f = open("out","r+")

    solution_aux = f.readline()
    f.close()
    solution_aux = solution_aux.split(" ")
    value = (int)(solution_aux[0])
    taken = [0] * nodeCount
    aux = 0
    for i in range (0, nodeCount):
   	 taken[i] = (int)(solution_aux[i])
     	 if (aux < taken[i]):
		aux = taken[i]
    value = aux +1
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))
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

