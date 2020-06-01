#######################################################################
#
# attribute.py
# -------------
#
# Description: Fuzzy concept of an attribute
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
from quantity_v2 import *
from modifier_v2 import *

DEG_TO_RAD = 0.01745329251994329576923690768489
RAD_TO_DEG = 57.295779513082320876798154814105

#--------------------------------------------------------------
# Sets up a attribute concept composed of qualitative values
class ATTRIBUTE(CONCEPT, MODIFIER):

    # holds the attribute quantities so it does not need to be re-initialized each time an attribute concept is created
    quantities_log = []
    quantities_circular = []

    # holds the initialized instances
    instances = []

    # list of sizes
    qualitative_values_log = [0, 2, 5, 10, 20, 35, 60, 100, 160, 250, 400, 600, 900, 1350, 1800]
    #qualitative_values_circular = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
    qualitative_values_circular = [-157.5, -135, -112.5, -90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180]
    #qualitative_values_circular = [0, 45, 90, 135, 180, 225, 270, 315]

    def __init__(self, type="", name="", copy=None):
        if copy:
            CONCEPT.__init__(self, name=copy.name)

            self.type = copy.type
            self.quantities = copy.quantities[:]
            self.degrees_of_membership = copy.degrees_of_membership[:]
            self.circular = copy.circular
            ATTRIBUTE.instances.append(self)

            self.true_values = []           # holds the values that are fuzzified
        else:
            CONCEPT.__init__(self, name=name)

            if not type:
                raise "type required for an Attribute instance"

            self.type = type

            # determine if circular
            if self.type[-2:].lower() == "_c":
                self.circular = True
            else:
                self.circular = False

            if self.circular:
                self.quantities = ATTRIBUTE.quantities_circular
            else:
                self.quantities = ATTRIBUTE.quantities_log
            self.degrees_of_membership = []
            ATTRIBUTE.instances.append(self)

            self.true_values = []           # holds the values that are fuzzified


        # checks if a attribute quantities have been initialized
        if not self.quantities_log:

            qualitative_values_log = ATTRIBUTE.qualitative_values_log

            # adds the quantitative quantities
            v1 = qualitative_values_log[0]
            v2 = qualitative_values_log[1]
            self.quantities_log.append(QUANTITY(v1,[-0.5,v1,v2],[0,1,0]))

            v1 = qualitative_values_log[0]
            v2 = qualitative_values_log[1]
            v3 = qualitative_values_log[3]
            self.quantities_log.append(QUANTITY(v2,[v1,v2,v3],[0,1,0]))

            for i in xrange(2, len(qualitative_values_log)-2):
                v1 = qualitative_values_log[i-2]
                v2 = qualitative_values_log[i]
                v3 = qualitative_values_log[i+2]
                self.quantities_log.append(QUANTITY(v2, [v1,v2,v3], [0,1,0]))

            v1 = qualitative_values_log[-4]
            v2 = qualitative_values_log[-2]
            v3 = qualitative_values_log[-1]
            self.quantities_log.append(QUANTITY(v2,[v1,v2,v3],[0,1,0]))

            v1 = qualitative_values_log[-3]
            v2 = qualitative_values_log[-1]
            self.quantities_log.append(QUANTITY(v2,[v1,v2],[0,1]))

            print self.quantities_log

        #----------------


        # checks if a attribute quantities have been initialized
        if not self.quantities_circular:

            qualitative_values_circular = ATTRIBUTE.qualitative_values_circular

            # adds the quantitative quantities

            for i in xrange(0, len(qualitative_values_circular)):
                v1 = qualitative_values_circular[i-2]
                v2 = qualitative_values_circular[i]
                end = i+2
                if end >= len(qualitative_values_circular):
                    end -= len(qualitative_values_circular)
                v3 = qualitative_values_circular[end]
                self.quantities_circular.append(QUANTITY(v2, [v1,v2,v3], [0,1,0], circular_range=[-180,180]))

            print self.quantities_circular

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
        return ATTRIBUTE(copy=self)



    def defuzzify(self):
        if len(self.degrees_of_membership)==0:
            raise "Nothing to defuzzify -> likely not initialized"

        if self.circular:
            # covert polar to cartesian, find vector average, convert cartesian to polar
            defuzz_value_x = 0
            defuzz_value_y = 0
            for val in zip(ATTRIBUTE.qualitative_values_circular, self.degrees_of_membership):
                defuzz_value_x += cos(val[0]*DEG_TO_RAD)*val[1]
                defuzz_value_y += sin(val[0]*DEG_TO_RAD)*val[1]
            return atan2(defuzz_value_y, defuzz_value_x)*RAD_TO_DEG
        else:
            total = 0
            defuzz_value = 0
            for val in zip(ATTRIBUTE.qualitative_values_log, self.degrees_of_membership):
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
##    def output(self,q):
##        #SS file stuff is sterling
##        #q is referenced from run_top_100_visuo.py
##        print "Qualitative attribute concept of type: ",
##        print self.type
##        print "----------------------------"
##        print " Quantitative values: " + str(self.true_values)
##        if self.degrees_of_membership:
##            for quantity, membership in zip(self.quantities, self.degrees_of_membership):
##                q.write(str(quantity) + ',' + str(membership) + '\n')
##                print " Value: %6s   -  Membership: %.4f" % (str(quantity), membership)
##            print
##        else:
##            print " < not initialized > "
    def output(self):
        print "Qualitative attribute concept of type: ",
        print self.type
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
        return "ATTRIBUTE GROUP"

    # runs instance as a function
    def __call__(self, value):
        self.fuzzify(value)

    # resets quantities
    @staticmethod
    def reset(): ATTRIBUTE.quantities = []
