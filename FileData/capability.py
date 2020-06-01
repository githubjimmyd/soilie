#########################################################################
#
# capability.py
# -------------
#
# Description:   Template class for a concept capability.  Each
#                concept has the ability to perform arbitrary 
#                capabilities (high level functions).  Any class
#                that conforms to this template can be used as a
#                capability for a concept.
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
#########################################################################


# methods that need should be implemented in 
class CAPABILITY:

    @staticmethod
    def initialize(obj):
        pass

    @staticmethod
    def init(obj, *argsL, **argsD):
        pass

    @staticmethod
    def make_capable(obj):
        pass

    @staticmethod
    def make_uncapable(obj):
        pass

    @staticmethod
    def receive(obj, com_sig):
        pass
    
    @staticmethod
    def add_link(obj, feature):
        pass

    @staticmethod
    def remove_link(obj, feature):
        pass

    @staticmethod
    def get_links(obj):
        return []

    @staticmethod
    def process(obj):
        pass
        
    @staticmethod
    def transmit(obj):
        pass
    
    @staticmethod
    def stats(obj):
        pass
