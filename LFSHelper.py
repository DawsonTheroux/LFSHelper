from os import listdir
from os.path import isfile, join
from os import stat
import 

extentions = []                  # Array of extentions.
binaryExtentions = ["bin","BIN"] #Array of binary extentions.
filesWithoutExtentions = []
pathsToFiles = []

# Converts the extention array to the LFS track command.
def listToLFSTrack(extentionArray):
    outputStr = "git lfs track "
    for i in extentionArray:
        outputStr += '"*.' + i + '" '
    for i in filesWithoutExtentions:
        outputStr += '"' + i + '" '
    return outputStr

# Converts the extention array to the BFG command.
def listToBFG(extentionArray):
    outputStr = 'java -jar <PATH TO BFG SCRIPT> "{'

    for i in extentionArray:
        outputStr += "*." + i
        if i != extentionArray[len(extentionArray) - 1]:
            outputStr += ","

    for i in filesWithoutExtentions:
        outputStr += "," + i

    outputStr += "} --no-blob-protection <PATH TO GIT REPOSITORY>"
    return outputStr

            
# Checks if a file is a binary.
def isBinaryFile(path):
    with open(path, 'rb') as f:
        for block in f:
            if b'\0' in block:
                return True
    return False

# Adds the extention to extArr if it does not exist.
def addToExtArr(extention):
    for i in extentions:
        if extention == i:
            return False
    extentions.append(extention)
    return True

def traverseDirectory(path):

    # Iterate over directories in the path.
    for f in listdir(path):
        if isfile(join(path, f)):

            extention = f.split(".")
            if addToExtArr(extention[-1]) and isBinaryFile(join(path,f)):
                if extention[-1] == extention[0]:
                    filesWithoutExtentions.append(f)
                    pathsToFiles.append(join(path,f))
                        
                else:
                    binaryExtentions.append(extention[-1])

        else:
            if f == ".git" or f == "info" or f == "lfs" or f == "refs" or f == "logs" or f == "objects" or f == "svn" or f == "branches" or f == "hooks": #Ignores all Git objects.
                continue
            
            else:
                traverseDirectory(path + "/" + f)
                

def printHelp():
    print("\n Usage: python BinaryFileFinder.py [-arg1] [-arg2]\n")
    print("    Arguments:\n")
    print("        -o <Output File> --OR-- --outputFile <Output File>            : Define an output file location. Will overwrite files with the same name.\n")
    print("        -r <Repository Location> --OR-- --repo <Repository Location>  : Define the repository location.\n")
    print("        --listToLFSTrack <List of extentions> [-o <Output File>]      : Converts a list of extentions to the git lfs track command.\n")
    print("        --listToBFG <List of extentions> [-o <Output File>]           : Converts a list of extentions to a BFG tool command.\n")

    
def getBinaryFileExtentions(outputFileName, pathToTraverse):
    try:
        traverseDirectory(pathToTraverse)
    except:
        print("\nRepository path < " + pathToTraverse + " > does not exist\n")
        return

    try:
        f = open(outputFileName, "w")
    except:
        print("\nUnable to create: " + outputFileName + "\n")
        return
        
    # Creates a list of extentions to be added to the file.
    f.write("\n--- ALL FILE EXTENTIONS: ---\n")
    outputStr = ""
    for ext in extentions:
        outputStr += ext + ","
    f.write(outputStr + "\n\n")

    # Adds the binary file extentions to the list.
    f.write("--- BINARY FILE EXTENTIONS: ---\n")
    outputStr = ""
    for i in range(len(binaryExtentions)):
        outputStr += binaryExtentions[i] + ","
    f.write(outputStr + "\n")

    #adds the binary files without extentions.
    f.write("\n--- BINARY FILES WITHOUT EXTENTIONS: ---\n")
    for i in range(len(filesWithoutExtentions)):
        f.write(filesWithoutExtentions[i] + " : " + pathsToFiles[i] + " \n")
        
    f.write("\n--- BFG command with Binary extentions: ---\n")
    f.write(listToBFG(binaryExtentions))

    f.write("\n\n--- lfstrack command with Binary extentions: ---\n")
    f.write(listToLFSTrack(binaryExtentions) + "\n")
    
    f.close()

def outputCommand(function, oFile, strList):
    lst = strList.split(",")
    if oFile == "binaryFileExtentions.txt":
        print(function(lst))
    else:
        f = open(oFile, "w")
        f.write(function(lst))
        f.close
        
def parseArgs():
    errorString = "    -- ERROR: Invalid arguments --\n    Use -h or --help for help"
    
    if len(sys.argv) <= 1:
        print(errorString)
        
    elif len(sys.argv) == 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--h":
            printHelp()
            
    else:
        repoIndex = 0
        outputFileIndex = -1
        lstToLFS = False
        lstToBFG = False
        lst = ""
        

        for i in range(len(sys.argv)):
            if sys.argv[i] == "-r" or sys.argv[i] == "--repo": repoIndex = i + 1
            if sys.argv[i] == "-o" or sys.argv[i] == "--outputFile": outputFileIndex = i + 1
            if sys.argv[i] == "--listToLFSTrack":
                lstToLFS = True
                lst = sys.argv[i+1]
            if sys.argv[i] == "--listToBFG":
                lstToBFG = True
                lst = sys.argv[i+1]
            
        if outputFileIndex == -1:
            outputName = "binaryFileExtentions.txt"
        else:
            outputName = sys.argv[outputFileIndex]

        if lstToLFS:
            outputCommand(listToLFSTrack, outputName, lst)
        elif lstToBFG:
            outputCommand(listToBFG, outputName, lst)
        elif repoIndex != 0 and outputFileIndex != 0:
            getBinaryFileExtentions(outputName, sys.argv[repoIndex])
        else:
            print(errorString)
            
def main():
    parseArgs()
                
if __name__ == "__main__":
    main()
