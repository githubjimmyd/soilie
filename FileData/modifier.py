#######################################################################
#
# modifier.py
# ------------
#
# Description: Gives concepts the ability to modify one another
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
from utilities import *
from attribute import *

path = "dist_demo\\"

TOLERANCE = 0.001                       # amount that the normalized concept distributions are allowed to be missaligned

class DISTRIBUTION_CONTAINER:
    def __init__(self, distribution):                
        self.update(distribution)
        
    def update(self, distribution=[]):
        if distribution:
            self.distribution = distribution
        
        if self.distribution:
            self.normalized_distribution = []
            total = 0
            
            for val in self.distribution:
                total += val
                
            for val in self.distribution:
                self.normalized_distribution.append(val/total)
            

    

class MOD_CONTAINER:
    def __init__(self, distribution=[], range=[], type="", cls=NOT_AVALIABLE):
        self.setDist(distribution, range)
        self.setClass(cls)
        self.count = 0
        self.type = type
        if not self.type:
            raise "There needs to be a type"
       
    # sets the distribution and range
    def setDist(self, distribution, range):
        if len(distribution) != len(range):
            raise "Mod distribution does not match mod range"
        
        self.distribution = distribution
        self.range = range
        
    # returns self as an iteratable object
    def __iter__(self):
        self.count = 0
        return self
        
    # used for getting the next value of the iteration
    def next(self):        
        if self.hasNext():
            self.count += 1
        else:
            self.count = 0
            raise StopIteration
        return (self.distribution[self.count-1], self.range[self.count-1])
        
    # checks if object has another value not iterated over yet
    def hasNext(self):
        return len(self.distribution) > self.count      
        
    # sets the class type
    def setClass(self, cls):
        self.cls = cls
        
    # returns the distribution and range
    def getDist(self):
        return (self.distribution, self.range)
    
    # returns the class
    def getClass(self):
        return self.cls

    # checks if the distribution is valid
    def isValid(self):
        return (len(self.distribution) == len(self.range)) and (self.distribution != []) and (self.cls != NOT_AVAILABLE)

    # returns a string representation
    def __repr__(self):     
        return "-- MOD_CONTAINER --\nDistribution: " + str(self.distribution) + "\nRange: " + str(self.range) + "\nClass: " + str(self.cls) + "\n"
    
    # outputs string represenation
    def output(self):
        print "-- Printing MOD_CONTAINER --"
        print "Distribution:", self.distribution
        print "Range:", self.range
        print "Class:", self.cls
        
        
# a type of concept that modifies objects.  
class MODIFIER:
    def __init__(self):    
        # checks for errors    
        if not isAnInstance(self):
            raise "Invalid modifer: not an instance"
        if hasattr(self, "degrees_of_membership"):
            raise "Invalid modifier: no self.degrees_of_membership found"        
        if hasattr(self, "quantities"):
            raise "Invalid modifier: no self.quantities found"

    
    # outputs degrees of membership distribution to a file
    def write_membership_distribution(self, filename, title="", extra_info=[]):
        if filename[-5:] != ".dist":
            filename = filename + ".dist"
        if path != filename[0:10]:
            filename = path + filename
            
        f = open(filename,"w")
        f.write('title="' + title + '"\n')
        XAV_FOUND = False
        for info in extra_info:
            f.write(info)
            if "xAxisVals" in info:
                XAV_FOUND = True
        if not XAV_FOUND:
            if hasattr(getClass(self),"qualitative_values"):
                f.write("xAxisVals=" + str(getClass(self).qualitative_values)+"\n")
        for val in self.degrees_of_membership:
            f.write(str(val)+"\n")
        f.close()
        
   
    # checks if reference is of the same type and size as self
    def check(self, reference):
        #checks if reference is of the same type and size as self
        if isAnInstance(reference):
            if getClass(reference) != getClass(self):
                raise "Invalid modifier or reference modifier: not of the same class:\n  self: " + str(getClass(self)) + "\n  ref:  " + str(getClass(reference))
        else:
            raise "Invalid modifier reference\n    " + str(reference)       
        
        # checks that reference has appropriate lists
        if not (hasattr(reference, "degrees_of_membership") and hasattr(reference, "quantities")):
            raise "Invalid reference: Object does not have correct attributes"
        
        
    # normalizes a distribution such that the sum of all degrees of membership equals 1
    # this is useful to allow the modifier distribution to know what percentages of the
    # reference concept to multiply by.  (See documentation)
    @staticmethod
    def normalize_distribution(ref_dist):
        normalized_distribution = []
        total = 0
        
        for val in ref_dist:
            total += val
        
        for val in ref_dist:
            normalized_distribution.append(val / total)
            
        return normalized_distribution
        
    # returns the constructed modifier
    def get_modifier(self, reference):
            
        # checks that the reference in appropriate
        self.check(reference)
        if len(self.degrees_of_membership) != len(reference.degrees_of_membership):
            raise "Invalid membership size"
        
        # normalizes the reference distribution
        normalized_ref_distribution = self.normalize_distribution(reference.degrees_of_membership)
        
        degrees_mod  = []               # holds the modifier coefficients       
        
        # builds the modifier
        for (curDeg, refDeg) in zip(self.degrees_of_membership, reference.degrees_of_membership):
            if refDeg:
                degrees_mod.append(curDeg/refDeg)
            else:
                degrees_mod.append(0)
                
        mod = MOD_CONTAINER(degrees_mod, normalized_ref_distribution, self.type, getClass(self))
        
        return mod

    # as the name suggests
    def set_membership_from_distibution_file(self, filename):
        distribution = extract_distribution(filename)
        if len(distribution) != len(self.quantities):
            print "distribution:", distribution
            print "len(distribution):", len(distribution)
            print "quantities:  ", self.quantities
            print "len(quantities):  ", len(self.quantities)
            raise "Error: file distribution is not the same size as the quantities"
        else:
            self.degrees_of_membership = distribution
            
            
    # builds a new concept from a modifier and a reference
    @staticmethod
    def modify(modifier, reference):
        # modifier is an instance of MOD_CONTAINER
        # reference is an instance of MODIFIER and CONCEPT
        
        # checks if modifier is empty
        if not modifier.hasNext():
            raise "Invalid Modifier:  Modifier is empty"            
        
        # extracts the class to be created
        cls = modifier.getClass()
        
        # creates a new concept
        concept = cls(modifier.type)
                      
        # checks that the reference is appropriate
        concept.check(reference)
        
        mod_count = 0       # amount of modifier distribution that still needs to be matched up with the reference distribution
        ref_count = 0       # amount of reference distribution that still needs to be matched up with the modifier distribution
        
        
        ref_dist = reference.degrees_of_membership                          # reference distribution
        ref_dist_normalized = MODIFIER.normalize_distribution(ref_dist)     # normalized (area under distribution = 1) reference distribution
        new_dist = []                                                       # holds a new modifier distribution that is adjust to the reference
        
        mod_dist, mod_dist_range = modifier.getDist()                       # gets the modifier's dist. values and the ranges that those values are applicable to
        
#        print "ref dist"
#        print ref_dist
#        print
#        print "ref dist normal"
#        print ref_dist_normalized
#        print 
#        print "mod dist"
#        print mod_dist
#        print
#        print "mod dist range"
#        print mod_dist_range
#        print
        
        # counter (for debugging)     
        i = 0
             
        #print "building modifier"
        mod_val, mod_count = modifier.next()        # gets the fist modifier value and the range that it is applicable
        
        # iterates through each of the reference's range values 
        for ref_range in ref_dist_normalized:
            
            store = []                  # stores information to create the a new distirbution value
            
            ref_count += ref_range      # keeps track of remaining amount of unaccounted for reference range
            
            # uncomment for debugging purposes 
#            i += 1
#            print "========================================================"
#            print i
#            print "            ref count", ref_count, "   mod count", mod_count            
            
            # case where there is more reference range unaccounted for
            while(ref_count > mod_count):
                store.append((mod_count, mod_val))    
#                print "mod_count", mod_count
#                print "ref_count", ref_count            
                ref_count -= mod_count              
#                print "ref_count", ref_count
                
#                print "--------------------------------------------------"
#                print "ref > mod"
                            
                if modifier.hasNext():
                    mod_val, mod_count = modifier.next()
#                    print "            ref count", ref_count, "   mod count", mod_count
                else:
                    mod_val, mod_count = (0, TOLERANCE/2)
                    global mod_count   
                    print "        has no more"                    
            
            # case where there is more modifier range unaccounted for
            if (ref_count <= mod_count):
#                print "--------------------------------------------------"
#                print "ref <= mod"
                store.append((ref_count, mod_val))
                mod_count -= ref_count
                ref_count = 0.0
#                print "            ref count", ref_count, "   mod count", mod_count
                
            # produces a new value for the adjusted modifier distribution
            total_count = 0
            total_val = 0
            #print "store", store,
            for count, val in store:
                total_count += count
                total_val += count*val
            if total_count:
                total_val /= total_count
            else:
                total_val = 0
            #print total_val
            #print
            new_dist.append(total_val)          # adds the new value to the new distribution       
    
        # checks if all of the reference's ranges have been accounted for
        if abs(ref_count) > TOLERANCE:
            raise "Improper match up -- ref_count =", ref_count
        
        # checks if all of the modifier's ranges have been accounted for
        while(modifier.hasNext()):
            v,c = modifier.next()
            mod_count += c
        if abs(mod_count) > TOLERANCE:
            raise "Improper match up -- mod_count =", mod_count
        
        # creates the new distribution to be return by multiplying the values of the adjusted modifier distribution by the reference distribution
        for m_val, r_val in zip(new_dist, ref_dist):
            print "Mod Val:", m_val, "    Ref Val", r_val
            concept.degrees_of_membership.append(m_val * r_val)
                    
        
        return concept      # returns the new concept
    
    
