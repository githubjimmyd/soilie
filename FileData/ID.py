#######################################################################
#
# ID.py
# -----
#
# Description:  Gives a unique identification label to all objects  
#               controlled by the simulated parallel processor. 
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


# returns whether 'cls' is a class 
def isAClass(cls):
    return hasattr(cls, '__bases__')

# returns whether 'obj' is an instance of a class
def isAnInstance(obj):
    return hasattr(obj, '__class__')

#----------------------------------------------------
# ID Generator
class ID:  

    # initializes ID class
    value = 0               # unique value added to each name to insure each name is different
    unknown = 0             # id counter for unknown items
    ids = {}                # dictionary of concepts  ->   ids[key] = concept
#    WeakValueDictionary

    # finds the ID Key for a given concept if it exists
    @staticmethod
    def findKey(obj):
        # searches dictionary for 'obj'
        if obj in ID.ids.values():
            for x in ID.ids:
                k,v = x
                if v == obj:
                    return k
        return None

    # generates a unique name for a given concept
    @staticmethod
    def generate(obj, name=""):

        # checks if an ID was previously generated
        # if so, return previously generated ID
        foundIdent = ID.findKey(obj)
        if foundIdent != None: return foundIdent
            
        # generates a unique id  (different depending on what kind of concept is passed in
        if isAnInstance(obj):
            
            # identifies the type of concept
            if isinstance(obj, CONCEPT):
                ident = "%s_%s%d" % (str(obj.typeOf), name, ID.value)
                ID.value += 1
            elif isinstance(obj, SLOT):
                ident = "%s_%s%d" % ('Slot', name, ID.value)
                ID.value += 1
            elif isinstance(obj, CONTAINER):
                ident = "%s_%s%d" % ('Chunk', name, ID.value)
                ID.value += 1
            elif isinstance(obj, LINK):
                ident = "%s_%s%d" % ('Link', name, ID.value)
                ID.value += 1
            elif isinstance(obj, LINK_UNI):
                ident = "%s_%s%d" % ('Link (UNI) ', name, ID.value)
                ID.value += 1
            elif isinstance(obj, LINK_MULTI):
                ident = "%s_%s%d" % ('Link (MULTI) ', name, ID.value)
                ID.value += 1
            else:
                ident = "%s_%s%d" % (obj.__class__.__name__, name, ID.value)
                ID.value += 1
        elif isAClass(obj):
            ident = "%s_%s%d" % (obj.__name__, name, ID.value)
        else:
            ident = "<?>_%s%d" % (str(name), ID.unknown)
            ID.unknown += 1
        
        ID.addID(ident, obj)        # adds the ID/concept to the ids dictionary
        return ident

    # adds an ID/concept pair to the ids dictionary
    @staticmethod
    def addID(anID, obj):
        if obj not in ID.ids.values():
            ID.ids[anID] = obj

    # removes an entry from the dictionary
    @staticmethod
    def remID(anID):
        if anID in ID.ids:
            del ID.ids[anID]

    # returns the ids dictionary
    @staticmethod
    def getIDs():
        return ID.ids


from concept import *
from slot import *
from utilities import *
from links import *