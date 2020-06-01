######################################################################
#
# velocity.py
# -----------
#
# Description: Holds the innate qualitative concept of movement speed
#
#
# Author:   Justin Singer
#           Institute of Cognitive Science
#           Carleton University
#           justinsinger@cmail.carleton.ca
#
######################################################################



from __future__ import division
from concept import *
from quantity import *
from modifier import *
from numpy import *

#--------------------------------------------------------------
# Sets up a velocity concept composed of qualitative values
class VELOCITY(CONCEPT, MODIFIER):

    # holds the velocity quantities so it does not need to be re-initialized
    quantities = []

    # holds the initialized instances
    instances = []

    # list of linear velocities
    linear_qualitative_values = [0, 2, 5, 10, 20, 35, 60, 100, 160, 250, 400, 600, 900, 1350, 1800]

    # list of angular velocities
    angular_qualitative_values = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, -157.5, -135, -112.5, -90, -67.5, -45, -22.5]

    def __init__(self, typeOf="VELOCITY", name=""):
        

    
