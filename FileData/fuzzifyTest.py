#######################################################################
#
# Fuzzy Test.py
# ----------------
#
# Description: Tests the fuzzification 
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

from __future__ import division

# represents a concept that is yet undetermined
class NOT_AVALIABLE:
    def __init__(self, *extra):   
        self.relations = []
        self.isA = self
        self.typeOf = "NOT_AVALIABLE"
        self.name = "Not Avaliable"
        self.slot = []
        self.initialized = True

    def initialize(self):
        pass
    def recieve(self, *extra):
        pass
    def process(self, *extra):
        pass
    def __call__(self, *argsL, **argsD):
        pass

NA = NOT_AVALIABLE()                # instance of the undetermined concept


# qualitative quantity instantiated through fuzzy set theory.  Each element (quantitative number) has a distribution
# representing the degree of membership
class QUANTITY:
    def __init__(self, name, members, degrees_of_membership, circular_range=[]):
        
        if circular_range:
            # checks if circular range is okay
            if len(circular_range) == 2:                                    
                if circular_range[0] == circular_range[1]:
                    raise 'Invalid "circular_range"'
            else:
                raise 'Invalid "circular_range"'
                
            # puts values in order
            if circular_range[0] > circular_range[1]:
                temp = circular_range[0]
                circular_range[0] = circular_range[1]
                circular_range[1] = temp
                
            # makes sure members are within circular range
            range_size = circular_range[1] - circular_range[0]
            for i in xrange(len(members)):
                while(members[i] <= circular_range[0]):
                    members[i] += range_size
                while(members[i] > circular_range[1]):
                    members[i] -= range_size

        if len(members) != len(degrees_of_membership): raise str("Invalid quantity instantiation -- " + "Members: " + len(members) + "    Weights: " + len(degrees_of_membership))
        self.name = str(name)                                   # concept's name
        self.circular_range = circular_range                    # min and max boundaries for circular range
        self.members = members                                  # elements in the set
        d = dict(zip(self.members, degrees_of_membership))
        self.members.sort()
        self.degrees_of_membership = [d[key] for key in self.members]  # distribution

        # TODO: RELACE CONTINUOUS FUNCTION WITH DESCRETE VALUES so values can be added better
        #   ALSO: change add function

        lastMember=NA
        for mem in self.members:
            if mem == lastMember:
                raise "Invalide quantity instantiation:  Duplicate member found"
            lastMember = mem
       

    # whether quantities is on a linear dimension
    def isLinear(self): return self.circular_range == []

    # whether quantities is on a circular dimension
    def isCircular(self): return len(self.circular_range) == 2
            

    # merges two quantities
    def merge(self, q):
        raise "Not implemented yet"     # may not be the best way to merge
        # TODO: sort
        if isinstance(q, QUANTITY):
            if len(q.members) != len(q.degrees_of_membership): raise str("Invalid merge quantity -- " + "Members: " + len(q.members) + "    Weights: " + len(q.degrees_of_membership))
            self.members.extend(q.members)
            self.degrees_of_membership.extend(q.degree_of_membership)
        else:
            raise str("Unable to merge quantity")


    # expands the broadness of the quantity
    def add(self, q, strength):
        raise "Not implemented yet"     # may not be the best way to add
        # TODO: sort
        if not strength:
            self.members.append(q)
            self.degrees_of_membership.append(strength)

    # sorts the members and the degrees of membership with respect to the order of the members
    def sort(self):
        d = dict(zip(self.members, self.degrees_of_membership))
        self.members.sort()
        self.degrees_of_membership = [d[key] for key in self.members]


    # returns the degree of membership of a given quantitative value 
    def fuzzify(self, val):
        
        # for a circular dimension
        if self.circular_range:
            range_size = self.circular_range[1] - self.circular_range[0]
            
            # puts val in proper range
            while(val <= self.circular_range[0]):
                val += range_size
            while(val > self.circular_range[1]):
                val -= range_size

            # unravel quantity
            linearized_members = [(mem-range_size) for mem in self.members]
            linearized_members.extend(self.members)
            linearized_members.extend([(mem+range_size) for mem in self.members])
            
            linearized_degrees = self.degrees_of_membership[:]
            linearized_degrees.extend(self.degrees_of_membership)
            linearized_degrees.extend(self.degrees_of_membership)

            for i in xrange(len(linearized_members)-1):
                if val >= linearized_members[i] and val < linearized_members[i+1]:
                    ratio = (val - linearized_members[i]) / (linearized_members[i+1] - linearized_members[i])
                    return (linearized_degrees[i] * (1-ratio)) + (linearized_degrees[i+1] * (ratio))

        # for a linear dimension
        else:
            if val < self.members[0]:
                return self.degrees_of_membership[0]
            elif val >= self.members[-1]:
                return self.degrees_of_membership[-1]
            else:
                for i in xrange(len(self.members)-1):
                    if val >= self.members[i] and val < self.members[i+1]:
                        ratio = (val - self.members[i]) / (self.members[i+1] - self.members[i])
                        return (self.degrees_of_membership[i] * (1-ratio)) + (self.degrees_of_membership[i+1] * (ratio))
            

    # returns string representation of self
    def __repr__(self):
        return self.name

    # outputs the representation of itself
    def output(self):
        print "Quantity"
        print " name: " + str(self.name)
        if self.circular_range:
            print " circular"
        else:
            print " linear"
        print " range: " + str(zip(self.members, self.degrees_of_membership))
        print
#--------------------------------------------------------------
# Sets up a attribute concept composed of qualitative values
class ATTRIBUTE():

    # holds the attribute quantities so it does not need to be re-initialized each time an attribute concept is created
    quantities = []
    
    # holds the initialized instances
    instances = []

    # list of sizes
    qualitative_values = [0, 2, 5, 10, 20, 35, 60, 100, 160, 250, 400, 600, 900, 1350, 1800]
    
    def __init__(self, atype="", name="", copy=None):
        if copy:
    
            self.atype = copy.atype
            self.quantities = ATTRIBUTE.quantities
            self.degrees_of_membership = copy.degrees_of_membership[:]
            ATTRIBUTE.instances.append(self)
            
            self.true_values = []           # holds the values that are fuzzified 
        else:
                
            if not type:
                raise "type required for an Attribute instance"
            
            self.type = type
            self.quantities = ATTRIBUTE.quantities
            self.degrees_of_membership = []
            ATTRIBUTE.instances.append(self)
            
            self.true_values = []           # holds the values that are fuzzified 


        # checks if a attribute quantities have been initialized
        if not self.quantities:

            qualitative_values = ATTRIBUTE.qualitative_values
                   
            # adds the quantitative quantities
            v1 = qualitative_values[0]
            v2 = qualitative_values[1]
            self.quantities.append(QUANTITY(v1,[-0.5,v1,v2],[0,1,0]))

            v1 = qualitative_values[0]
            v2 = qualitative_values[1]
            v3 = qualitative_values[3]
            self.quantities.append(QUANTITY(v2,[v1,v2,v3],[0,1,0]))
            
            for i in xrange(2, len(qualitative_values)-2):
                v1 = qualitative_values[i-2]
                v2 = qualitative_values[i]
                v3 = qualitative_values[i+2]
                self.quantities.append(QUANTITY(v2, [v1,v2,v3], [0,1,0]))

            v1 = qualitative_values[-4]
            v2 = qualitative_values[-2]
            v3 = qualitative_values[-1]
            self.quantities.append(QUANTITY(v2,[v1,v2,v3],[0,1,0]))
                                   
            v1 = qualitative_values[-3]
            v2 = qualitative_values[-1]
            self.quantities.append(QUANTITY(v2,[v1,v2],[0,1]))
            
            print self.quantities


    def copy(self):
        return ATTRIBUTE(copy=self)
        
    

    def defuzzify(self):
        if len(self.degrees_of_membership)==0:
            raise "Nothing to defuzzify -> likely not initialized"
        total = 0
        defuzz_value = 0
        for val in zip(ATTRIBUTE.qualitative_values, self.degrees_of_membership):
            defuzz_value += val[0]*val[1]
            total += val[1]
        if total == 0:
            return 0
        else:
            return defuzz_value/total
            

    # turns a quantitative value in to a qualitative value
    def fuzzify(self, value):
        self.true_values.append(value)
        membership = []
        for quantity in self.quantities:
            membership.append(quantity.fuzzify(value))
            
        size = len(self.true_values)
        
        if size < 2:
            self.degrees_of_membership = membership
        else:
            for i in xrange(len(self.degrees_of_membership)):
                self.degrees_of_membership[i] = self.degrees_of_membership[i]*((size-1)/size) + membership[i]*(1/size)
         
                    
    # add distribution
    def add_attribute(self, attrib):
        self.true_values.append(attrib.defuzzify())                    
        size = len(self.true_values)
        
        if size < 2:
            self.degrees_of_membership = attrib.degrees_of_membership[:]
        else:
            for i in xrange(len(self.degrees_of_membership)):
                self.degrees_of_membership[i] = self.degrees_of_membership[i]*((size-1)/size) + attrib.degrees_of_membership[i]*(1/size)
                        

    # outputs the fuzzy values
    def output(self):
        if self.degrees_of_membership:
            for quantity, membership in zip(self.quantities, self.degrees_of_membership):
                print " Value: %5s   -  Membership: %.4f" % (str(quantity), membership)
            print
        else:
            print " < not initialized > "
        

    # outputs the fuzzy values
    def output2(self):
        print "["
        if self.degrees_of_membership:
            for quantity, membership in zip(self.quantities, self.degrees_of_membership):
                print "(%s, %f)" % (str(quantity), membership)
            print "]"
            print
        else:
            print " < not initialized > "
            
    def output3(self):
        print self.degrees_of_membership

    # removes membership data
    def clear(self):
        self.degrees_of_membership = []
        self.true_values = []

    # returns a representation of itself    
    def __repr__(self):
        return "ATTRIBUTE GROUP"

    # runs instance as a function
    def __call__(self, value):
        self.fuzzify(value)

    # resets quantities
    @staticmethod
    def reset(): ATTRIBUTE.quantities = []


    # inputs the values of the distribution()
    def setMembershipValues(self):
        self.clear()
        print
        print "Enter membership values (one per line):"
        for i in xrange(len(self.quantities)):
            self.degrees_of_membership.append(float(raw_input().strip()))
        self.true_values.append(self.defuzzify())
        
        print
        print "Distribution: "
        self.output3()
        print
        print "Defuzzified value:"
        print self.defuzzify()
        print
    

attrib = ATTRIBUTE()
print
print "Creates fuzzy distributions"
print "---------------------------"
print
print "Input a number to be added to the distribution"
print "Other options: h (help), c (clear), q (quit), d (defuzzify), "
print "               p (print), s (set) membership values"
print
while(True):
    val = raw_input().strip()
    if val == 'q' or val == 'quit':
        break
    elif val == 'c' or val == 'clear':
        attrib.clear()
    elif val == 'd' or val == 'defuzzify':
        print attrib.defuzzify()
    elif val == 'p' or val == 'print':
        print attrib.output()
    elif val == 's' or val == 'set':
        attrib.setMembershipValues()
    elif val == 'h' or val == 'help':
        print
        print "Input a number to be added to the distribution"
        print "Other options: h (help), c (clear), q (quit), d (defuzzify), "
        print "               p (print), s (set) membership values"
        print
    else:
        try:
            number = int(val)
            attrib.fuzzify(number)
            attrib.output3()
                                 
        except:
            print
            print "invalid command"
            print


    
