#######################################################################
#
# utilities.py
# ------------
#
# Description:  Contains a number of classes and functions that are    
#               used as utilities by objects in various modules.
#
# Author:   Jonathan Gagne
#           Institute of Cognitive Science
#           Carleton University
#           jgagne2@connect.carleton.ca
#
# For:      Undergraduate Thesis
# Supervisor: Dr. Jim Davies
#
#######################################################################


NEVER = 0
ALWAYS = -1

# returns whether 'cls' is a class 
def isAClass(cls):
    return hasattr(cls, '__bases__')

# returns whether 'obj' is an instance of a class
def isAnInstance(obj):
    return hasattr(obj, '__class__')
    
# returns the class name
def getClass(obj):
    if isAnInstance(obj):
        return getattr(obj, "__class__")
    else:
        return None
        

# represents a concept that is yet undetermined
class NOT_AVALIABLE:
    def __init__(self, *extra):   
        self.relations = []
        self.isA = self
        self.typeOf = "NOT_AVALIABLE"
        self.name = "Not Avaliable"
        self.slot = []
        self.initialized = True
##    def __getattr__(self, name):
##        if name == "slot":
##            self.slot = SLOT(typeOf=self)
##        else:
##            print "Invalid attribute in NA: " + name

    def initialize(self):
        pass
    def recieve(self, *extra):
        pass
    def process(self, *extra):
        pass
    def __call__(self, *argsL, **argsD):
        pass

NA = NOT_AVALIABLE()                # instance of the undetermined concept

# -----------------------------
# holds information
class CONTAINER:
    def __init__(self, isIn = NA, typeOf=NA):
        self.typeOf = typeOf
        self.isIn = isIn


# gets distribution from file
def extract_distribution(filename, path=".\\", extra_info=False):

    connections = []
    if filename == -1: return []
    
    extra = []

    if path not in filename:
        filename = path+filename
    # opens the file for reading
    FILE = open(filename, "r")  
    # reads each line of the file one by one
    for line in FILE:
        line = line.strip() 
        if line:       
            if "=" not in line:
                connections.append(float(line))
            else:
                if extra_info:
                    extra.append(line)
                else:
                    print "Extra info ignored -> " + line
    FILE.close()

    if extra_info:
        return (connections, extra)
    else:
        return connections
