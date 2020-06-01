#######################################################################
#
# size.py
# -----------
#
# Description: Fuzzy concept of size  
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
from concept2 import *
from quantity import *
from modifier import *

#--------------------------------------------------------------
# Sets up a size concept composed of qualitative values
class SIZE(CONCEPT, MODIFIER):

    # holds the size quantities so it does not need to be re-initialized each time a SIZE concept is created
    quantities = []
    
    # holds the initialized instances
    instances = []

    # list of sizes
    qualitative_values = [0, 2, 5, 10, 20, 35, 60, 100, 160, 250, 400, 600, 900, 1350, 1800]
    
    def __init__(self, name="", copy=None):
        if copy:
            CONCEPT.__init__(self, name=copy.name)
    
            self.quantities = SIZE.quantities
            self.degrees_of_membership = copy.degrees_of_membership[:]
            SIZE.instances.append(self)
            
            self.true_values = []           # holds the values that are fuzzified 
        else:
            CONCEPT.__init__(self, name=name)
    
            self.quantities = SIZE.quantities
            self.degrees_of_membership = []
            SIZE.instances.append(self)
            
            self.true_values = []           # holds the values that are fuzzified 

        # checks if a size quantities have been initialized
        if not self.quantities:

            qualitative_values = SIZE.qualitative_values
                   
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

        #----------------

        # adds links from each node to every other node
##        self.weights = []
##        
##        length = len(self.quantities)        # number of nodes
##        i = 0    
##        while i < length:
##            
##            ii = 0
##            while ii < length:
##                if i != ii:    
##                    weight = (-1)*abs(ii-i)/1000
##                    self.quantities[i].add_link(LINK(self.nodes[ii], weight))
##                ii += 1
##            i += 1

    def copy(self):
        return SIZE(copy=self)

    def defuzzify(self):
        if len(self.degrees_of_membership)==0:
            raise "Nothing to defuzzify -> likely not initialized"
        total = 0
        defuzz_value = 0
        for val in zip(SIZE.qualitative_values, self.degrees_of_membership):
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
                    


    # outputs the fuzzy values
    def output(self):
        print "Qualitative size concept"
        print "----------------------------"
        print " Quantitative values: " + str(self.true_values)
        if self.degrees_of_membership:
            for quantity, membership in zip(self.quantities, self.degrees_of_membership):
                print " Value: %5s   -  Membership: %.4f" % (str(quantity), membership)
            print
        else:
            print " < not initialized > "

    # removes membership data
    def clear(self):
        self.degrees_of_membership = []
        self.true_values = []

    # returns a representation of itself    
    def __repr__(self):
        return "SIZE GROUP"

    # runs instance as a function
    def __call__(self, value):
        self.fuzzify(value)

    # resets quantities
    @staticmethod
    def reset(): SIZE.quantities = []
