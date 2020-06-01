#######################################################################
#
# processor.py
# ------------
#
# Description:  Simulated parallel processor that allows all concepts  
#               function as computational units simultaneously. 
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
from utilities import NEVER
from utilities import ALWAYS

MAX_LOOP_PER_SEC  = 15          # max number of cycles per second
MAX_STATS_PER_SEC = ALWAYS      # statistical refresh rate per second
# ---------------------------------------------------
# class that simulates a parallel processor 
#   used to process concepts each stage all at once
#   as opposed to serial processing
class PROCESSOR:
    
    instance = None                       # string containing python name of the an instance of PROCESSOR

    # returns whether an instance has been initialised
    @staticmethod
    def isinitialized():
        return PROCESSOR.instance != None

    # returns the name of the instance processor
    @staticmethod
    def get_processor():
        if PROCESSOR.isinitialized():
            return PROCESSOR.instance         # evaluates the string containing the python name of the instance processor
        else:
            raise "Processor not initialised"


    # constructor
    def __init__(self, name):

        self.name = name                # reference name of processor (NOTE: should be set to a string containing the name of the processor)
        PROCESSOR.instance = self       # sets the reference name of the instance
        
        self.threads = []               # stores the objects to be processed in parallel (simulated)
        
        # statistics
        self.loop_counter = 0           # number of processor loops
        self.old_loop_counter = 0       # number of processor loops at last stats display
        self.clock = time.Clock()       # used to keep track of how much time has passed since last stats display
        self.fps = time.Clock()         # used to control the max cycles per second of the processor
        if MAX_STATS_PER_SEC != ALWAYS and MAX_STATS_PER_SEC != NEVER:
            time.set_timer(pyg_vars.POLLCLOCK, 1000/MAX_STATS_PER_SEC)       # sets stats refresh rate
            event.post(event.Event(pyg_vars.POLLCLOCK))                      # causes an event to be posted for each stats refreshing
        

    # adds a concept to the processor threads
    def add_concept(self, concept, auto=False):
        
        # checks if concept is not already added
        if concept not in self.threads:
            
            # initialized concept if not already done
            if not concept.isinitialized():
                concept.initialize()

            # adds concept as thread
            self.threads.append(concept)

            if not auto:
                concept.set_special(True)           # sets the concept to be special if it is manually added

            # if verbose mode is set to True
            if config.VERBOSE:
                # prints whether concept was manually added or automatically added
                if auto:
                    print str(concept) + " was automatically added"
                else:
                    print str(concept) + " was manually added"

        else:
            # if verbose mode is set to True
            if config.VERBOSE:
                print str(concept) + " has already been added ***"


    # removes a concept from the treads
    def remove_concept(self, concept):
        if concept in self.threads:
            self.threads.remove(concept)


    # Main processing loop
    # iterates through the thread list and processs each one once
    def run(self):

        loop = True        
        while loop:

##            # checks each concept's links to see if any new concepts need to be added
##            for c in self.threads:
##                for link in c.links:
##
##                    if link.target not in self.threads:
##                        self.threads.append(link.target)
##                        print str(link.target) + " was automatically added"

            # makes sure each concept is initialized
            for c in self.threads:
                if c.initialized == False:
                    c.initialize()

            # allows each concept to process any recieved activations
            for c in self.threads:
                c.process()

            # allows each concept to transmit its activation
            for c in self.threads:
                c.transmit()

            self.loop_counter += 1              # adds one to the loop counter

  
            # checks the event queue for keys pressed and for a stats refresh event
            action = event.poll()               # gets keys pressed
            if action.type == KEYDOWN:
                # exit on next loop
                if action.key == K_ESCAPE:      # checks if excape was pressed
                    loop = False
            
            if action.type == pyg_vars.POLLCLOCK or MAX_STATS_PER_SEC == ALWAYS:        # checks for a stats refresh event
                self.display_stats()
            

            self.fps.tick(MAX_LOOP_PER_SEC)     # ensures that processor is not running more then MAX_LOOP_PER_SEC


    # displays the stats to the screen
    def display_stats(self):

        time_stamp = self.clock.tick()          # amount of time since last stats display
        if time_stamp == 0:
            print "Timestamp: " + str(time_stamp)

        # renders text
        loop_total_text = pyg_vars.font1.render("Total # of Loops:     " + str(self.loop_counter) + " "*20, 1, white, black)
        if time_stamp != 0:
            loops_text = pyg_vars.font1.render("Loops / Sec:           %4.0f" % ((self.loop_counter-self.old_loop_counter)*1000/time_stamp) + " "*20, 1, white, black)

        currentY = 20
        # draws the stats to the screen
        if time_stamp != 0:
            pyg_vars.window.blit(loops_text, (20,currentY)) 
            currentY = currentY+pyg_vars.FONT_SIZE+3
        pyg_vars.window.blit(loop_total_text, (20, currentY))
        
        # starting x position of activations display
        initX = 10
        # starting y position of activations display           
        initY = currentY+pyg_vars.FONT_SIZE+15
        
        x=initX
        y=initY  
        
        # draws all concept's activations to screen
        for c in self.threads:

            text_list = c.stats()               # list containing rendered text
            if text_list == None: continue      # skips this iteration if there is no text to be displayed

            # displays the text line by line
            for rendered_text in text_list:
            
                # displays concept info to the monitor
                pyg_vars.window.blit(rendered_text, (x, y))
                # changes x and y values for the next concept
                y += pyg_vars.FONT_SIZE
                if y > (pyg_vars.window.get_height() - pyg_vars.FONT_SIZE - 10):
                    y = initY
                    x += 12*pyg_vars.FONT_SIZE
            
        display.update()                            # updates the display
        self.old_loop_counter = self.loop_counter   # stores the the number of loops to compare to next refresh

#-----------------------------------------------------------------------------

from colours import *
from pygame_init import *
from pygame import *
from config import *
