import sys

def readloglevel(level):
    if level == 0:
        findstr = "[ERR]"
    elif level == 1:
        findstr = "[WARN]"
    elif level == 2:
        findstr = "[VERBOSE]"
    elif level == 3:
        findstr = "[DEBUG]"
    else:
        printhelp()
        sys.exit()
    f = open("log.txt")
    a = f.read()
    g = a.splitlines()
    for h in g:
        if h.find(findstr) >- 1:
            print h

def readmaxloglevel(level):
    find = []
    if level >= 0:
        find.append("[ERR]")
    if level >= 1:
        find.append("[WARN]")
    if level >= 2:
        find.append("[VERBOSE]")
    if level >= 3:
        find.append("[DEBUG]")
    f = open("log.txt")
    a = f.read()
    g = a.splitlines()
    for h in g:
        for findstr in find:
            if h.find(findstr) > -1:
                print h



def printhelp():
    print "LGHT Log Filterer"
    print "Syntax: python logfilter.py <max|exclusive> <log no (max=3)>"

#Check to make sure the program isn't being used as a module
if __name__=='__main__':
    #Initalize the pygame library
    #Check to see if any arguments have been passed
    if len(sys.argv) != 3:
        printhelp()
        sys.exit()
    if sys.argv[1]=="max":
        readmaxloglevel(int(sys.argv[2]))
    elif sys.argv[1]=="exclusive":
        readloglevel(int(sys.argv[2]))
    else:
        printhelp()
