################################################
#
#  MAIN MODULE
# -------------
#
# Description:  * Main Program *
#               Initializes all other modules
#
# Author:   Jonathan Gagne
#           Institute of Cognitive Science
#           Carleton University
#           jgagne2@connect.carleton.ca
#
# For:      Undergraduate Thesis
# Supervisor: Dr. Jim Davies
#
################################################



# import python modules
from __future__ import division
from math import *
import sys
import traceback

# import visualization modules
from config import *
from parse import *
from command import *
from excitable import *
from pygame import *
from pygame_init import *
from processor import *
from task import *
from slot import *
from concept import *
from distance import *
from angle import *
from modifier import *

def main():

    try:
        pyg_init()
        
            # initializes the parallel processor
        cpu = PROCESSOR('cpu')          # sends the name of the reference variable as a string


##        orientation = CONCEPT.build("ORIENTATION")
##
##        tskcommand = COMMAND(capability=EXCITABLE, signal = 2)
##        exciteConcept = TASK(tskcommand, orientation, "Excitation")
##
##        cpu.add_concept(exciteConcept)
##        cpu.add_concept(orientation)

    
        if config.TRAINING_MODE:
            print " Training Mode"
            print "---------------"
            print
            concept = build_exemplar(config.TRAINING_FILE)
        else:
            print " Visualization Mode"
            print "--------------------"
            print
            aString = raw_input("Image: ").strip()                      # gets user input
            
            if not aString or aString == "quit":
                print "Quiting..."
                pyg_quit()  # removes display
                return          
            else:
                concept = CONCEPT.build_from_string(aString)
                

        print "--- STARTING ---"

        tskcommand = COMMAND(capability=EXCITABLE, signal = 4)
        exciteConcept = TASK(tskcommand, concept, "Excitation")

        cpu.add_concept(exciteConcept)
        cpu.add_concept(concept)
        
        if not config.DISTRIBUTION_DEMO_MODE:
            cpu.run()                   # starts the processor
        pyg_quit()                  # removes display
        
    except:
        # Displays a traceback when an exception is raised
        print "EXCEPTION RAISED"
        aType, value, trbk = sys.exc_info()
        print "".join(traceback.format_exception (aType, value, trbk))
        pyg_quit()  # removes display

    

#_____________________________________________________________________________
# checks if image.py is being run as a mondule or a main program.  if main, than runs main loop
if __name__ == "__main__" and config.RUNABLE:
    
    main()
    
    if config.DISTRIBUTION_DEMO_MODE:
        from distribution_demo import *
        
