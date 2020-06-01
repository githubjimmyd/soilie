#############################################################################
#
# slot.py
# -------
#
# Description:   A skeleton type representation of multi-concepts concepts.
#                See thesis for more details on slots.
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
#############################################################################


from utilities import NA
# used by the concept as a frame slot.
# When a concept has a slot, it is equivalent to having a "has-a" relation (COVLAN)
class SLOT:
    def __init__(self, isA = NA, typeOf = NA):

        self.name = ID.generate(self)
        self.isA = isA                  # reference to the concept stored in the slot
        self.typeOf = typeOf            # type of concept that fits in the slot
##        self.isIn = isIn              # reference to the super-slot
        self.slots = []                 # sub-slots
        #self.candidates = []           # list of tuple which store the name and weight of candidates for the slot
        self.iter_count = 0             # stores position for iteration object

        

    # adds a sub-slot
    def add(self, aSlot):
        self.slots.append(aSlot)
        return aSlot

    # returns the next slot in the iteration
    def next(self):
        if self.iter_count >= len(self.slots):
            self.iter_count = 0
#            print "Iter count: " + str(self.iter_count)
            raise StopIteration
        x = self.slots[self.iter_count]
        self.iter_count += 1
        return x

    # restarts the iteration
    def reset_iteration(self):
        self.iter_count = 0

    # returns an iterable object
    def __iter__(self):
        self.iter_count = 0
        return self

    def __repr__(self):
        return "Slot of type: " + str(self.typeOf)

    # returns the number of sub-slots
    def __len__(self):
        return len(self.slots)

    def __getitem__(self, k):
        return self.slots[k]

    def remove(self, x):
        if x in self.slots:
            self.slots.remove(x)
    def append(self, x):
        self.add(x)
    def extend(self, x):
        self.add(x)
    def index(self, x, *s):
        if len(s) == 0:
            return self.slots.index(x)
        elif len(s) == 1:
            return self.slots.index(x,s[0])
        elif len(s) == 2:
            return self.slots.index(x,s[0],s[1])
        else:
            print "Invalid number of parameter in SLOT.index()"
            return self.slots.index(x)
    def __contains__(self, x):
        return x in self.slots
    def not__contains__(self, x):
        return x not in self.slots
    def __add__(self, x):
        self.slots.append(x)
        return x
    def __sub__(self, x):
        if x in self.slots:
            self.slots.remove(x)
        return x

from ID import *