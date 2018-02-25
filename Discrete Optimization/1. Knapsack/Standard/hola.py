
import os
import subprocess
def solveIt(inputData):

    ### Writes the inputData to a temporary file
    tmpFileName = 'tmp.data'
    tmpFile = open(tmpFileName,'w')
    tmpFile.write(inputData)
    tmpFile.close()

#--------------------------------------------------------------------------------------------------
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

    ### Call your program, e.g. Test, with the file name as argument(s)
    process = subprocess.call(['./knap',"20"])
    print "Programa terminado"


    ### removes the temporary file (Optional)
    ### os.remove(tmpFileName)

    ### If you wish, you could further do any post-processing to stdout
    ### before returning the output
    return "Python terminado"



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

