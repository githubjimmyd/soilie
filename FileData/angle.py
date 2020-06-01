###############################################################
#
# angle.py
# --------
#
# Description:  Holds the innate qualitative concept of angle
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
###############################################################

from __future__ import division
from concept import *
from quantity import *
from modifier import *

# Sets up a angle concept composed of qualitative values
class ANGLE(CONCEPT, MODIFIER):

    # holds the angle quantities so it does not need to be re-initialized each time a angle concept is created
    quantities = []

    # holds the instances of ANGLE
    instances = []

    # list of angles
    qualitative_values = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180,
                          -157.5, -135, -112.5, -90, -67.5, -45, -22.5]
    
    def __init__(self, typeOf="ANGLE", name=""):
        CONCEPT.__init__(self, typeOf="ANGLE")
        
        self.quantities = ANGLE.quantities
        self.degrees_of_membership = []
        self.true_values = []                   # holds the values that are fuzzified
        ANGLE.instances.append(self)

        # "TODO: Change this so that i makes sense for the ANGLE concept !!"

        # checks if a distance quantities have been initialized
        if not self.quantities:

            qualitative_values = ANGLE.qualitative_values
            size = len(qualitative_values)

            for i in xrange(size):
                if i%2 == 0:
                    if i+2 >= size: x = i-size
                    else: x = i
                    v1 = qualitative_values[i-2]
                    v2 = qualitative_values[i]                    
                    v3 = qualitative_values[x+2]
                else:
                    if i+1 >= size: x = i-size
                    else: x = i
                    v1 = qualitative_values[i-1]
                    v2 = qualitative_values[i]
                    v3 = qualitative_values[x+1]

                self.quantities.append(QUANTITY(v2, [v1,v2,v3], [0,1,0], [-180,180]))
            
        
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
##                    self.quatities[i].add_link(LINK(self.nodes[ii], weight))
##                ii += 1
##            i += 1

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
        print "Qualitative distance concept"
        if self.degrees_of_membership:
            for quantity, membership in zip(self.quantities, self.degrees_of_membership):
                print "Value: %5s   -  Membership: %.4f" % (str(quantity), membership)
        else:
            print " < not initialized > "

##        # converts each qualitative angle into a node
##        self.nodes = []        
##        for val in self.values:
##            self.nodes.append(NODE(val, typeOf = "ANGLE"))
##
##        length = len(self.nodes)            # number of nodes in the angle group
##        connections = extract_connections("angles.txt")     # file which contains the weights of the links 
##        i = 0
##        
##        # adds links from each node to every other node with the weight of the links taken from the above file
##        while i < length:
##            aNode = self.nodes[i]
##            ii = i
##            for c in connections:
##                ii += 1
##                if ii >= length: ii = 0
##                aNode.add_link(LINK(self.nodes[ii], c))
##            i += 1

    # removes membership data
    def clear(self):
        self.degrees_of_membership = []
        self.true_values = []

    # returns a representation of itself    
    def __repr__(self):
        return "ANGLE GROUP"

    # runs instance as a function
    def __call__(self, value):
        self.fuzzify(value)

    # resets quatities
    @staticmethod
    def reset(): ANGLE.quantities = []
        
     

