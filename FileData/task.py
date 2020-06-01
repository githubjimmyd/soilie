#######################################################################
#
# task.py
# -------
#
# Description:  Sets up a visualisation task    
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


class TASK:
    def __init__(self, command, target, name=""):
        self.command = command
        self.target = target
        self.initialized = True
        self.special = False

        if name == "":
            self.name = ID.generate(self) 
        else:
            self.name = ID.generate(self, name)        

    def receive(self):
        pass

    def process(self):
        pass

    def transmit(self):
        self.target.receive(self.command)

    def stats(self):
        pass

    def isinitialized(self):
        return self.initialized
    def isspecial(self):
        return self.special
    def set_special(self, TruthVal):
        self.special = TruthVal

    # returns the string representation of the concept
    def __str__(self):
        return "<" + str(self.name) + ">"
    
from ID import *