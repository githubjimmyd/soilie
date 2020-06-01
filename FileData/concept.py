#######################################################################
#
# concept.py
# ----------
#
# Description: contains implementation of a concept 
#               
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


from command import *
from utilities import *
from excitable import *
from ID import *
from parse import *
from processor import *
from slot import *
from config import *

#==============================
# base class for concepts
class CONCEPT:

    # *** NOTE: This is temporary.
    #           It will be replaced by a "Concept Generator" which will supply the code
    #           to build an concept relative to the context
    MASTER_DIRECTORY = {}                   # a dictionary of all the concepts and there respective file
    DEFAULT_CAPABILITIES = [EXCITABLE]      # capabilities of unknown concepts
    
    def __init__(self, typeOf, name="", tree=None):
        self.typeOf = typeOf            # type of concept
        if name == "":
            self.name = ID.generate(self) # creates a name
        else:
            self.name = ID.generate(self, name)            
        self.initialized = False        # whether or not the concept has been initialized
        self.relations = []             # list of relations
        self.links = []                 # list of links
        self.unresolved = []
        self.capabilities = []          # list of the concept's capabilites
        self.containers = {}            # mapping of all capabilities containers  key = cls.__name__ : class container
        self.slot = SLOT(typeOf=typeOf)
        self.special = False
        self.tree = tree                # builds concept from tree template if available

##    # aligns the slots of concepts
##    def align_slots(self):
##
##        def compare_slots(slotP, slotS):
##
##            def compare_slots_helper(slotP, slotS, level):
##                for subslotP in slotP:
##                    
##            
##            value = 0
##            notFound = 0
##            found = 0
##            extra = 0
##            level = 0
##
##            notFound_val 
##            found_val
##            extra_val
##            level_modval
##
##            
##            
##
##        candidates = []
##        
##        featureList = []
##        for s in self.slot:            
##            if s.isA == NA:
##                featureList.append(CONCEPT.build(s.typeOf))
##
##        # get the mask of each slot's concept    
##        for s in self.slot:
##            if s.isA == NA:
##                matchValues = []
##                for feature in featureList:
##                    
##
##                # compare the mask's slots with the sub-slots of the slot
##                
##                for sub = self.slot

                

    def initialize(self):
        # Creates concepts to be filled in, if they do not exist.
        #
        # TODO: Currently it only fills in the first level.
        #       The sub-levels also need to be filled in.
        #       Set it up recursively.
        for s in self.slot:
            if s.isA == NA:
                feature = CONCEPT.build(s.typeOf)
                s.isA = feature
                #feature.isIn = self.slot
                self.add_link(feature)

     
        self.initialized = True

    def isinitialized(self):
        return self.initialized
    def get_name(self):
        return self.name
    def get_type(self):
        return self.typeOf
    def isspecial(self):
        return self.special
    def set_special(self, TruthVal):
        self.special = TruthVal


    # adds a capability to the concept (eg. EXCITABLE)
    def add_capability(self, cls):
        if cls not in self.capabilities:
            self.capabilities.append(cls)
            self.containers[cls.__name__] = CONTAINER(isIn=self, typeOf=cls)
            cls.init(self)

    # removes a capability for the concept
    def rem_capability(self, cls):
        if cls in self.capabilities:
            self.capabilities.remove(cls)
            del self.containers[cls.__name__]

    # returns the container the stores information for the given capability
    def get_container(self, cls):
        return self.containers[cls.__name__]


    # queues incomming transmittions
    def receive(self, command, capability=NA):
##        found = False
##
##        # checks if the concept is capable of interpreting the recieved command
##        for cap in self.capabilities:
##            if func in dir(cap):
##                cap.receive(self, func, *argsL, **argsD)        # delegate the command to the appropriate class
##                found = True
##
##        # checks if concept could not interpret command.  if so, put in the unresolved list
##        if not found:
##            self.unresolved.append((func, argsL, argsD))
            
        # *** create a search method ***

        # checks if 'command' is a COMMAND object
        if isinstance(command, COMMAND):
            capability = command.get_capability()
            if capability in self.capabilities:
                capability.receive(self, command)
        # othewise 'command' is actually just a signal
        else:
            if capability in self.capabilities:
                capability.receive(self, command)
        

    # adds a link to other nodes
    def add_link(self, concept):
#        self.links.append(aLink)

        # adds 'concept' to processor if one exists
        if PROCESSOR.isinitialized():                   # checks if a PROCESSOR has been initilized
            theCPU = PROCESSOR.get_processor()           # gets the reference name of the PROCESSOR instance            
            theCPU.add_concept(concept, auto=True)             # adds concept to processor

        # checks if any capabilities need to do processing
        for cap in self.capabilities:
            cap.add_link(self, concept)
        

##    # removes a link to other nodes
##    def remove_link(self, aLink):
##        if aLink in self.links:
##            self.links.remove(link)
##        # checks if any capabilities need to do processing
##        for cap in self.capabilities:
##            cap.remove_link(self)

    # processes all data received durin transmision stage.  *** Method is ran by PROCESSOR ***
    def process(self):
        # checks if any capabilities need to do processing
        for cap in self.capabilities:
            cap.process(self)

    # transmits all data to other concepts.  *** Method is ran by PROCESSOR ***
    def transmit(self):
        # checks if any capabilities need to do transmitting
        for cap in self.capabilities:
            cap.transmit(self)
            
    # gets stats to be displayed.  *** Method is ran by PROCESSOR ***
    def stats(self):
        
        statslist = []              # list of stats to be displayed by PROCESSOR
        
        # gets any stats from capabilities
        for c in self.capabilities:
            statslist.append(c.stats(self))

        return statslist

    # returns the string representation of the concept
    def __str__(self):
        return str(self.name)

#    # needs to be modified
#    @staticmethod
#    def mask(typeOf):
#        raise "Not Implemented"
#        if typeOf not in CONCEPT.MASTER_DIRECTORY:
#            print "Unable to concept mask '" + name +"', because concept could not be found"
#            return NA
#
#        fileN = CONCEPT.MASTER_DIRECTORY[typeOf]
#
#        # TODO: Make sure this works. Plus, make sure the hardcorded concepts are all good
#        # this meens it is a hardcoded concept        
#        if fileN[0] == '<' and fileN[-1] == '>':
#            # TODO: Implement this section
#            raise "NOT IMPLEMENTED: Mask of a hardcored concept"
#            
#        else:
#            mask = CONTAINER(typeOf=MASK)
#            # !!!!!! OUTDATED
#            CONCEPT.build_from_file(mask)
#            # --------------
#            return mask


    @staticmethod
    def build(typeOf):

        found = False               # whether concept has been found

        # replaces spaces with underscores
        typeOf = (typeOf.strip()).replace(" ", "_")

        # removes exterior brackets
        typeOfBracketless = "null void null"
        if len(typeOf) > 3:
            if typeOf[0] == "[" and typeOf[-1] == "]":
                typeOfBracketless = typeOf[1:-1]

        # builds concept if found in MASTER_DIRECTORY
        if typeOf in CONCEPT.MASTER_DIRECTORY:
            found = True
        elif typeOfBracketless in CONCEPT.MASTER_DIRECTORY:
            found = True
            typeOf = typeOfBracketless            
        if found == True:
            fileN = CONCEPT.MASTER_DIRECTORY[typeOf]

            # TODO: Make sure this works. Plus, make sure the hardcorded concepts are all good
            # this meens it is a hardcoded (innate) concept        
            if fileN[0] == '<' and fileN[-1] == '>':
                fileN = fileN[1:-1]
                try:
                    c = eval(fileN)
                except NameError:
                    if config.VERBOSE:
                        print fileN + " Not found -> attempting to import files"
                    code = "from " + fileN.lower() + " import *"
                    exec(code)
                    c = eval(fileN)
                return c()
                
            else:
                concept = CONCEPT(typeOf)
                concept.build_from_file()
                return concept
            
        # builds blank concept if is not found in MASTER_DIRECTORY
        else:
            # TODO:  have it attempt to build concept
            if config.VERBOSE:
                print "Unable to find concept '" + typeOf +"', attempting to build a blend"
            return NA


    # builds concepts from a string representation
    @staticmethod
    def build_from_string(text="", tree=None):
        if text != "":            
            tree = PARSER.build_tree(text)                  # builds a tree structure representation of string            
        if tree == None:
            raise "Invalid parameters sent to CONCEPT.build_from_string()\nText: " + str(text) + "\nTree: " + str(tree)
        if tree.is_root():
                tree.covlan(indent=True)                    # prints the covlan representation
        concept = CONCEPT.build(tree.name)              # builds concept if concept has been perceived before
        # creates a concept if it has not been perceived before
        if concept == NA:
            concept = CONCEPT(tree.name)
            # adds default capabilities
            for cap in CONCEPT.DEFAULT_CAPABILITIES:
                concept.add_capability(cap)
            # adds slots and subslots recursively
            for child in tree.get_children():
                childConcept = CONCEPT.build_from_string(tree=child)                # builds subconcepts
                aSlot = SLOT(isA=childConcept,typeOf=child.get_name())              # creates a slot for the subconcept
                concept.slot.add(aSlot)                                             # adds the slot
                if EXCITABLE in CONCEPT.DEFAULT_CAPABILITIES:                       # adds EXCITABLE links if it has capability
                    concept.add_link(childConcept)
                    
        return concept

    # recursive function that builds a concept from a string representation                
    @staticmethod
    def build_concept(supr = None, aString = "Null"):

        # uncomment block below if the concept should be wrapped in an sImage
##        if supr == None:
##            supr = CONCEPT("sImage", "sImage")
##        supr.contained_concepts.append(CONCEPT.build_concept(supr, aString))
##            return supr

        thisConcept = CONCEPT(name=aString)                     # creates a concept from the string
          
        parsing_error = "Parsing Error"             # string displayed if there is a parsing error

        aString = CONCEPT.clean_name(aString)                   # cleans up aString (removes extra spaces and outside brackets

        if not ('[' in aString or ']' in aString or ' ' in aString):        # if concept doesnt contain any concepts, return concept
            return thisConcept
                
        substring = []                                          # is a temporay string representing a subconcept
        english_name = []                                       # english name of the concept
        encapsulated_concept = False                            # flags if an encapsulated concept is found
        non_encap_concept = False                               # flags if a non encapsulated concept is found
        bracket_count = 0                                       # counts levels of encapsulation
        
        # analizes aString character by character
        for char in aString:

            english_name.append(char)                           # builds english rep. of concept's name
            substring.append(char)                              # builds english rep. of subconcept's name

            # checks for encapsulation and counts levels
            if char == '[':
                bracket_count += 1
                encapsulated_concept = True
            if char == ']':
                bracket_count -= 1

            # checks for end of encapsulation and creates concept from encapsulation
            if bracket_count == 0 and encapsulated_concept == True:
                thisConcept.contained_concepts.append(CONCEPT.build_concept(thisConcept, substring))  # creates concept
                encapsulated_concept = False                    # turns off encapsulation flag
                char = None                                     # prevents char from being read by non-encapsulation detection
                substring = []                                  # clears substring
                    
            # checks for a parsing error
            if bracket_count < 0:
                raise parsing_error

            # checks for a non-encapsulation concept
            if encapsulated_concept == False:                   # does not break consider non-encap. concepts with encapsualation
                if char != ' ' and char != None:                # check for begining onf non-encap. concepts
                    non_encap_concept = True
                if non_encap_concept == True and char == ' ':                   # check for end of non-encap. concepts
                    thisConcept.contained_concepts.append(CONCEPT(substring))   # creates non-encap. concept    
                    non_encap_concept = False                                   # clears non-encap. flag
                    substring = []                                              # clears substring
        if non_encap_concept == True:                                           # checks for a final non-encap concept
            thisConcept.contained_concepts.append(CONCEPT(substring))           # creates non-encap. concept
        
        return thisConcept                                      #  returns created concept


    def build_from_file(self, code_object=None, other_concepts={}):

        if code_object:
            code = code_object.code
        else:
            if "<" in self.typeOf: raise "Cannot build concept of type '" + self.typeOf + "'"
            filename = CONCEPT.MASTER_DIRECTORY["__conceptpath__"] + CONCEPT.MASTER_DIRECTORY[self.typeOf]
            code = self.read_concept_file(filename)
        
        featureDictionary = {}
        key2InstanceDictionary = {}
        slotDictionary = {}

        print "Building " + str(code)
        mode = None
        for codeLine in code:
            if "#" in codeLine:
                codeLine = codeLine[0:codeLine.index("#")]
            codeLine = codeLine.strip()
            if len(codeLine) == 0: continue         # skips empty lines

            if "<" in codeLine and ">" in codeLine: mode = codeLine
            elif mode == "<exec>":
                if config.VERBOSE:
                    print codeLine
                    if "self(23)" in codeLine:
                        print self.__class__ 
                exec(codeLine)
            elif mode == "<declaration>":
                # Not implemented yet
                pass
            elif mode == "<capabilites>":
                self.add_capability(eval(codeLine))
            elif mode == "<feature list>":
                if ":" in codeLine:
                    key = codeLine[:codeLine.index(":")].strip()
                    if codeLine.find("->") != -1:
                        feature = codeLine[codeLine.index(":")+1:codeLine.index("->")].strip()
                        instance = codeLine[codeLine.index("->")+2:].strip()
                        if instance:
                            if other_concepts:
                                if instance in other_concepts:
                                    key2InstanceDictionary[key] = other_concepts[instance]
                                else:
                                    raise "Invalid Exemplar file\n" + str(instance) + " not found in training file"
                            else:
                                raise "other_concepts not supplied"
                                                
                    else:
                        feature = codeLine[codeLine.index(":")+1:].strip()
                    featureDictionary[key] = feature            #stores the name of te feature as string
                else:
                    raise "Invalid Format in Concept File: " + filename
            elif mode == "<slots>":                
                if ":" in codeLine and "." in codeLine:
                    key = codeLine[:codeLine.index(":")]
                    slot = codeLine[codeLine.index(".")+1:]
                    subslot = codeLine[codeLine.index(":")+1:codeLine.index(".")]

                    if subslot == "":
                        feature = featureDictionary[slot]
                        aSlot = SLOT(typeOf=feature)        # creates a new slot of feature type
                        slotDictionary[key] = aSlot
                        self.slot = aSlot                   # NOTE: variable 'self.slot' is not the same as 'slot'

                    else:
                        feature = featureDictionary[slot]
                        if slot in key2InstanceDictionary:   # if there is an instance supplied
                            instance = key2InstanceDictionary[slot]
                            aSlot = SLOT(isA=instance,typeOf=feature)        # creates a new slot of type feature
                        else:
                            aSlot = SLOT(typeOf=feature)        # creates a new slot of type feature
                        
                        slotDictionary[subslot].add(aSlot)  # adds a subslot
                        slotDictionary[key] = aSlot         # adds the slot to the slot dictionary

                else:
                    raise "Invalid Format in Concept File: " + filename
            elif mode == "<relations>":
                pass


    @staticmethod
    def read_concept_file(filename):
        FILE = open(filename, "r")
        code = FILE.readlines()
        FILE.close()
        return code

    
    

#=================================
# container class storing the 
# code read from a instance file
class CODE_OBJECT:
    def __init__(self, name):
        self.name = name
        self.typeOf = NA
        self.code = []

    def __repr__(self):
        return self.name


# builds an exemplar from a sample file
def build_exemplar(samplefile):

    # puts path in filename
    if CONCEPT.MASTER_DIRECTORY["__samplepath__"] not in samplefile:
        filename = CONCEPT.MASTER_DIRECTORY["__samplepath__"] + samplefile

    # reads the code from the sample file
    complete_code = CONCEPT.read_concept_file(filename)

    code_objects = []           # list of code objects
    current_obj = None           # points to the current object being created
    exemplar_concepts = {}      # dictionary of concept names and actual instances

    # runs through each line of the code
    for codeLine in complete_code:

        # cleans up code
        if "#" in codeLine:
            codeLine = codeLine[0:codeLine.index("#")]
        codeLine = codeLine.strip()
        if len(codeLine) == 0: continue         # skips empty lines

        # signals a new object in the code
        if codeLine[:4] == "def " and codeLine[-1:] == ":" and len(codeLine) > 5:   # start of concept
            current_obj = CODE_OBJECT(codeLine[4:-1].strip())
            code_objects.append(current_obj)
            declaration = False

        elif current_obj:
            # flags code is outside declaration section
            if codeLine[0] == '<' and codeLine[-1] == '>':
                declaration = False

            # flags code is in declaration section
            if codeLine == "<declaration>":
                declaration = True

            # sets type of concept
            if codeLine[:6] == "typeOf" and codeLine.find("=")!=-1 and declaration:   # determines the type of concept
                current_obj.typeOf = codeLine[codeLine.index("=")+1:].strip()

            # puts code in code object
            current_obj.code.append(codeLine)

    print code_objects

    # runs through each code object
    for obj in code_objects:        
        CLASS_CONCEPT = CONCEPT

        if obj.typeOf in CONCEPT.MASTER_DIRECTORY:
            foo = CONCEPT.MASTER_DIRECTORY[obj.typeOf.strip()]
            if foo[0] == '<' and foo[-1] == '>':
                print foo + " ***"
                try:
                    CLASS_CONCEPT = eval(foo[1:-1])
                except NameError:
                    if config.VERBOSE:
                        print foo[1:-1] + " Not found -> attempting to import files"
                    code = "from " + foo[1:-1].lower() + " import *"
                    exec(code)
                    CLASS_CONCEPT = eval(foo[1:-1])
                
        concept = CLASS_CONCEPT(obj.typeOf, obj.name)
        exemplar_concepts[obj.name] = concept


    for obj in code_objects:
        concept = exemplar_concepts[obj.name]
        concept.build_from_file(obj, exemplar_concepts)

        # adds default capabilities to concepts
        for cap in CONCEPT.DEFAULT_CAPABILITIES:
                concept.add_capability(cap)
        # adds links to children
        for childSlot in concept.slot:
            if EXCITABLE in CONCEPT.DEFAULT_CAPABILITIES:                       # adds EXCITABLE links if it has capability
                if childSlot.isA != NA:
                    concept.add_link(childSlot.isA)

    
    return exemplar_concepts[code_objects[0].name]      # returns the root of the file




# creates the master list of concepts
# Note: no concepts can begin with double underscores
def init_concept_class():
    CONCEPT.MASTER_DIRECTORY["__conceptpath__"] = "concepts\\"
    CONCEPT.MASTER_DIRECTORY["__samplepath__"] = "samples\\"

    FILE = open("CONCEPT_MASTER_LIST.txt", "r")
    for codeLine in FILE:
        if "#" in codeLine:
                codeLine = codeLine[0:codeLine.index("#")]
        codeLine = codeLine.strip()
        if len(codeLine) == 0:
            continue
        
        # make sure that list does not have reserved commands in concept names
        if codeLine.find("__") == 0:
            pyg_quit()
            raise "Invalid Master List Exception 1"

        # parses info
        if ":" in codeLine:
            name = codeLine[:codeLine.index(":")].strip()
            path = codeLine[codeLine.index(":")+1:].strip()
            CONCEPT.MASTER_DIRECTORY[name] = path
        else:
            pyg_quit()
            raise "Invalid Master List Exception 2"

# builds the MASTER_DIRECTORY of concepts
init_concept_class()

