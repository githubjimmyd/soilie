##############################################################################
#
# quantity.py
# -----------
#
# Description:   Fuzzy set representation of a dectected qualitative quantity
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
##############################################################################

from __future__ import division
from utilities import NA

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
