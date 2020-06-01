#######################################################################
#
# excitation.py
# -------------
#
# Description:  Capability that allows concepts to perform 
#               spreading activation.
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


MIN_EXCITE_THRESHOLD = 0.01         # concepts with activations under this are considered inactive
STABLE_THRESHOLD = 0.000001         # concepts with changes in activation less then this are considered to have converged

# sets the standard deviation for Gaussian interference on the signal  (0 = no interference)
#STD_DEV = 0
STD_DEV = .000005

class EXCITABLE:

    excitables = []     # list of all concepts that are excitable
    
    @staticmethod
    def init(obj, decayR = 0.8):

        c = obj.get_container(EXCITABLE)       
        
        c.excitation = 0             # level of activation
        c.old_exc = 0                # level of previous activation
        c.decay_rate = decayR        # decay rate of activation
        c.queue = []                 # activations to be transmitted
        c.links = []                 # list of activation links
                
        c.active = False             # whether the node is active
        c.stable = True              # whether the node has converged

        if obj not in EXCITABLE.excitables:
            EXCITABLE.excitables.append(obj)

    @staticmethod
    def make_capable(obj):
        obj.add_capability(EXCITABLE)

    @staticmethod
    def make_uncapable(obj):
        obj.rem_capability(EXCITABLE)

##    @staticmethod
##    def command(obj, func, *argsL, **argsD):
##        c = obj.get_container(EXCITABLE)
##        c.func(obj, *argsL, **argsD)

    @staticmethod
    def receive(obj, com_sig):
        c = obj.get_container(EXCITABLE)
        c.queue.append(com_sig)        
    
    @staticmethod
    def set_excitation(obj, value):
        c = obj.get_container(EXCITABLE)
        c.excitable.excitation = value

    @staticmethod
    def get_excitation(obj):
        c = obj.get_container(EXCITABLE)
        return c.excitation

    @staticmethod
    def add_link(obj, feature):
        c = obj.get_container(EXCITABLE)

        aLink = LINK(feature, EXCITABLE)
        aLink.init_code("self.strength = .8")        
        aLink.filter_code("signal *= self.strength")
        c.links.append(aLink)

    @staticmethod
    def remove_link(obj, feature):
        c = obj.get_container(EXCITABLE)
        # TODO: Implement remove_link()
        pass

    @staticmethod
    def get_links(obj):
        c = obj.get_container(EXCITABLE)
        return c.links

    # the processor runs this method to allow the node to process information from the receive queue
    @staticmethod
    def process(obj):

        c = obj.get_container(EXCITABLE)

        num_processed = 0
        totalStr = 0
        
        # processes activations in the queue
        for com_sig in c.queue:
            # if com_sig is a command, extract signal and store it as an excitation strength
            if isinstance(com_sig, COMMAND): strength = com_sig.get_signal()
            # else if com_sig is already a signal, store it an excitation strength
            else: strength = com_sig
            
            totalStr += strength        # adds excitation to total
            num_processed += 1          # counts the number of items in the queue that are processed
        c.queue = []                # clears the queue

        # determines whether the concept should be excited or inhibited
        excite_flag = 1
        if totalStr < 0:
            totalStr *= -1
            excite_flag = -1

        # adds the log of the activations to the activation level
        c.excitation += excite_flag * log(totalStr + 1)      

        # checks if the concept's activations have converged
        if abs(c.old_exc - c.excitation) < STABLE_THRESHOLD:
            c.stable = True
        else:
            c.stable = False

        # checks if the concept should be active
        if abs(c.excitation) < MIN_EXCITE_THRESHOLD:
            c.active = False
        else:
            c.active = True
        
        c.old_exc = c.excitation          # stores value of excitation to compare to the next cycle

        
    # the processor runs this method to allow the node to transmit its activation to other concepts
    @staticmethod
    def transmit(obj):

        c = obj.get_container(EXCITABLE)
        
        num_transmitted = 0                     # amount of activations transmitted
        
        for link in c.links:                 # sends activation to each linked concept
            if STD_DEV == 0: link.send(c.excitation)            # no noise
            else: link.send(c.excitation+gauss(0,STD_DEV))      # additive gaussien noise
            num_transmitted += 1

        # allows the concept to decay
        c.excitation *= c.decay_rate

        # sets excitation to 0 if it is less then the MIN_EXCITE_THRESHOLD
        #if obj.excitation < MIN_EXCITE_THRESHOLD:
        #    obj.exciation = 0

    # stats to be displayed
    @staticmethod
    def stats(obj):

        c = obj.get_container(EXCITABLE)

        # case when concept is special
        if obj.isspecial():
            if c.stable:          # checks if concept has converged
                exc_colour = r_w
            elif not c.active:        # checks if concept in inactive
                exc_colour = red            
            else:                   # default display colour
                exc_colour = lred
                
        # case when concept is NOT special
        else:            
            if c.stable:          # checks if concept has converged
                exc_colour = b_w
            elif not c.active:        # checks if concept in inactive
                exc_colour = grey            
            else:                   # default display colour
                exc_colour = white

        # renders activation level as text then returns it
        return pyg_vars.font1.render(str(obj) + ":  " + "%f" % c.excitation + " "*20, 1, exc_colour, black)

from colours import *
from command import *
from random import gauss
from math import *
from links import *
from pygame_init import *