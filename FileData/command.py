#######################################################################
#
# command.py
# ----------
#
# Description:   COMMAND is a general purpose container class used to
#                hold information for transmission between concepts.
#                A command can a complex block of data or even a
#                simple excitation value.               
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




from utilities import NA

#-----------------------------------
# holds info for command transmision
class COMMAND:
    
    # POSSIBLE PARAMETERS ARE:
    # source, target, capability, signal, func, argsL, argsD
    def __init__(self, **argsDict):


        # initializes parameters
        if "source" in argsDict: self.source = argsDict['source']
        else: self.source = NA
        if "capability" in argsDict: self.capability = argsDict['capability']
        else: self.capability = NA
        if "signal" in argsDict: self.signal = argsDict['signal']
        else: self.signal = NA
        if "func" in argsDict: self.func = argsDict['func']
        else: self.func = NA
        if "argsL" in argsDict: self.argsL = argsDict['argsL']
        else: self.argsL = NA
        if "argsD" in argsDict: self.argsD = argsDict['argsD']
        else: self.argsD = NA
        if "target" in argsDict: self.target = argsDict['target']
        else: self.target = NA
        


    # copies itself (used for transmission to new targets)
    def copy(self):
        return COMMAND(source=self.source, target=self.target, capability=self.capability, signal=self.signal, func=self.func, argsL=self.argsL, argsD=self.argsD)

    ## Get and Set methods ---------------
    def get_source(self):
        return self.source
    def set_source(self, source):
        self.source = source

    def get_target(self):
        return self.target
    def set_target(self, target):
        self.target = target

    def get_capability(self):
        return self.capability
    def set_capability(self, cap):
        self.capability = cap

    def get_signal(self):
        return self.signal
    def set_signal(self, signal):
        self.signal = signal

    def get_function(self):
        return self.func
    def set_function(self, func):
        self.func = func

    def get_arguments(self):
        return (self.argsL, self.argsD)
    def set_arguments(self, argsL=[], argsD={}):
        self.argsL = argsL
        self.argsD = argsD
    ## End of Get and Set methods section --------
