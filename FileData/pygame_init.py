#######################################################################
#
# pygame_init.py
# --------------
#
# Description:  - Intializes pygame components  
#               - De-initializes pygame components
#               - Stores pygame variables
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

from config import *

class pyg_vars:
    initialized = False
    SIZE_X=1200
    SIZE_Y=680
    FONT_SIZE=18
    DISABLE_DISPLAY = False
    
    @staticmethod
    def isinitialized():
        return pyg_vars.initialized

def pyg_quit():
    print "de-initializing..." 
    if not pyg_vars.DISABLE_DISPLAY:
        display.quit()  # removes display

def pyg_init():    
    
    # initializing imports
    display.init()
    font.init()

    # initialization
    display.set_caption("Visual Imagination Simulator")                         # sets title of window
    pyg_vars.window = display.set_mode((pyg_vars.SIZE_X, pyg_vars.SIZE_Y), RESIZABLE)      # displays a window
    pyg_vars.font1 = font.Font(None, pyg_vars.FONT_SIZE)                        # creates a font
    pyg_vars.POLLCLOCK = USEREVENT + 1                      # determines an ID for the stats event refresh
    event.pump()                                            # helps the program interact with the OS
    pyg_vars.initialized = True
   

if hasattr(config, "pyg_vars_SIZE_X"):
    pyg_vars.SIZE_X = getattr(config, "pyg_vars_SIZE_X")
if hasattr(config, "pyg_vars_SIZE_Y"):
    pyg_vars.SIZE_Y = getattr(config, "pyg_vars_SIZE_Y")
if hasattr(config, "pyg_vars_FONT_SIZE"):
    pyg_vars.FONT_SIZE = getattr(config, "pyg_vars_FONT_SIZE")

import sys
from pygame import *
import traceback
