#######################################################################
#
# dist_graph_demo.py
# --------------------
#
# Description:  Graphs Distributions 
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

from __future__ import division
from pygame import *
from time import sleep
from math import *
from probability import *
from colours import *
from utilities import extract_distribution
import os


# *** NOTE:  INPUTTED FILENAMES CANNOT START OR END WITH A SPACE (ERROR WILL OCCUR)

# initializing imports
display.init()
font.init()

B_COLOUR = white    # background colour
F_COLOUR = black    # foreground colour

WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600

DEFAULT_X = 20
DEFAULT_Y = 350

DEFAULT_DELAY = 0.05
DELAY_ALLOWED = True    # whether delay is allowed
scale = 1.05

# gets size of distribution
size = 31
start = -3
end   = 3
  
directory = "dist_demo//" 

class PRIMARIES:
    def __init__(self):
        self.primaries = []
        self.position = 0

    def getCurrent(self):
        if self.position >= len(self.primaries):
            self.position = len(self.primaries)-1
        if self.position < 0:
            self.position = 0   
        return self.primaries[self.position]
    
    def getNext(self):
        self.position += 1
        if self.position >= len(self.primaries):
            self.position = len(self.primaries)-1
        #self.primaries[self.position].reset()
        return self.primaries[self.position]

    def getPrevious(self):
        self.position -= 1
        if self.position < 0:
            self.position = 0
        #self.primaries[self.position].reset()
        return self.primaries[self.position]

    def __iter__(self):
        return self.primaries.__iter__()

    def reset(self):
        self.position = 0

    def add(self, dist):
        self.primaries.append(dist)
        

class PRIMARY_DIST:
    def __init__(self, filename, path=".\\"):
        self.name = filename[:-5]
        self.filename = filename
        self.path = path
        self.secondaries = []
        self.position = 0

    def getName(self):
        return self.name
    def getFilename(self):
        return self.filename
    def getPath(self):
        return self.path
    def getSecondaries(self):
        return self.secondaries
    def reset(self):
        self.position = 0

    def addSecondary(self, dist):
        self.secondaries.append(dist)

    def getCurrent(self):
        # checks if to position is in range
        if self.position > len(self.secondaries):
            self.position = len(self.secondaries)
        if self.position < 0:
            self.position = 0

        # returns distribution at position
        if self.position == 0:
            return extract_distribution(self.getFilename(), self.getPath(), extra_info=True)
        else:
            return extract_distribution(self.secondaries[self.position-1].getFilename(), self.getPath(), extra_info=True)
    
    def getNext(self):
        self.position += 1
        return self.getCurrent()
    
    def getPrevious(self):
        self.position -= 1
        return self.getCurrent()

    def __iter__(self):
        return self.secondaries.__iter__()

class SECONDARY_DIST:
    def __init__(self, filename, path=".\\"):
        self.filename = filename
        self.path = path
        self.primary = filename[:filename.find("&")]
        self.name = filename[filename.find("&")+1:filename.find(".")] + " " + self.primary

    def getName(self):
        return self.name
    def getPrimary(self):
        return self.primary
    def getFilename(self):
        return self.filename
    def getPath(self):
        return self.path


## gets distribution from file
#def extract_distribution(filename=-1):
#
#    connections = []
#    if filename == -1: return []
#
#    title = ""
#    # opens the file for reading
#    if directory not in filename:
#        filename = directory + filename
#    FILE = open(filename, "r")  
#    # reads each line of the file one by one
#    for line in FILE:
#        if "=" in line:
#            try:
#                exec(line)
#            except Exception, val:
#                print "EXCEPTION RAISED: " + str(val) 
#        else:
#            connections.append(float(line))
#    FILE.close()
#    return (connections, title)



# bar graph of a list
class Bar_Graph:
    
    # constructor
    def __init__(self, graph_list, title='', X_AXIS_VALS=[], sizeX = 600, sizeY = 200, print_values = True):
        self.title = title
        self.values = graph_list            # the heights of the bar graph are taken from the list
        self.sizeX = sizeX                  # width of the bars
        self.sizeY = sizeY                  # height of the bars (muliplied by values)
        self.print_values = print_values    # whether the values should be printed (not implemented)
        self.delay = DEFAULT_DELAY          # draw delay in seconds

        self.maxValue = max(self.values)    # gets max height
        self.minValue = min(self.values)    # gets min height
        if X_AXIS_VALS:
            self.X_AXIS_VALS = X_AXIS_VALS
        else:
            self.X_AXIS_VALS = range(len(self.values))
        self.title = title

        self.drawn = False                  # whether the graph is currently drawn
        
        self.old_values = []                # old values to be erased (used for clear)
        self.old_sizeX = self.sizeX         # old width (used for clear)
        self.old_sizeY = self.sizeY         # old height (used for clear)
        self.old_x = 0                     # old x location of graph (used for clear)
        self.old_y = 0                     # old y location of graph (used for clear)
        self.old_print_values = print_values    # old print of values option (used for clear)

    # updates graph values
    def update_values(self, graph_list, extra_info):
        
        title = ""
        xAxisVals = range(len(graph_list))
        for x_info in extra_info:
            try:
                exec(x_info)
            except Exception, val:
                print "Line ignored: " + str(val) 
        
        self.values = graph_list
        self.title = title
        self.X_AXIS_VALS = xAxisVals

    # draws the graph onto the screen at x, y.        
    def draw(self, x=DEFAULT_X, y=DEFAULT_Y, colour = F_COLOUR, delay = True, update = False):

        if not DELAY_ALLOWED:
            delay = False

        self.maxValue = max(self.values)    # gets max height
        self.minValue = min(self.values)    # gets min height

        if self.maxValue > -self.minValue:
            self.maxV = self.maxValue
        else:
            self.maxV = -self.minValue
        
        # clears graph first if it is alread drawn
        if self.drawn:
            self.clear(update = True)

        # hold the current state (used for clear)
        self.old_values = self.values[:]
        self.old_sizeX = self.sizeX
        self.old_sizeY = self.sizeY
        self.old_print_values = self.print_values
        self.old_x = x
        self.old_y = y
        self.colour = colour

        self.drawn = True

        # draws a reference dot
        draw.line(window, grey, (10,73), (10,74), 2)

        # draws title
        textTitle = font1.render(self.title+" "*50, 1, colour, B_COLOUR)
        window.blit(textTitle, (100,80))
        
        xpos = x                    # position marker for x
        length = len(self.values)
        # draws each bar one by one
        for val,xVal in zip(self.values,self.X_AXIS_VALS):            
            draw.rect(window,colour,(xpos,y-(val/self.maxV)*self.sizeY,self.sizeX//length,(val/self.maxV)*self.sizeY+1))
            text_val = transform.rotate(font2.render("%.5f" % val, True, lred), 270)
            x_val = transform.rotate(font2.render(str(xVal)+"   ", True, colour, B_COLOUR), 270)
            if self.print_values:
                if val < 0:
                    mod = -55
                else:
                    mod = 10
                window.blit(text_val, (xpos+(self.sizeX//length)/2-8,y+mod))     # draws the value under bar
                window.blit(x_val,(xpos+(self.sizeX//length)/2-8,y-40-self.sizeY))           # draws x-axis val
            
            xpos = xpos + self.sizeX//length + 3        # sets position for next bar
            
            if delay and not update:                           # delays draw
                display.update()
                sleep(self.delay)

        if not delay or update:
            display.update()
        
    # clears the bar graph (redraws with black as default)
    def clear(self, colour = B_COLOUR, delay = True, update = False):

        if not DELAY_ALLOWED:
            delay = False

        length = len(self.values)

        # clears if graph is drawn
        if self.drawn:
            
            #draw.rect(window,B_COLOUR,(0,0,WINDOW_SIZE_X,WINDOW_SIZE_Y ))
            
            xpos = self.old_x               # x position marker
            #draw.rect(window,B_COLOUR,(xpos, self.old_y-40-self.old_sizeY, 800, 40))
            # clears each bar
            for val,xVal in zip(self.values,self.X_AXIS_VALS):
                draw.rect(window,colour,(xpos, self.old_y-(val/self.maxV)*self.old_sizeY, self.old_sizeX//length, (val/self.maxV)*self.old_sizeY+1))
                text_val = transform.rotate(font2.render("%.5f" % val, True, colour, B_COLOUR), 270)
                x_val = transform.rotate(font2.render(str(xVal)+"   ", True, colour, B_COLOUR), 270)                
                if val < 0:
                    mod = -55
                else:
                    mod = 10
                window.blit(text_val, (xpos+(self.old_sizeX//length)/2-8,self.old_y+mod))     # draws the value under bar
                window.blit(x_val,(xpos+(self.old_sizeX//length)/2-8,self.old_y-40-self.old_sizeY))           # draws x-axis val           
            
            
                xpos = xpos + self.old_sizeX//length + 3        # increases position marker for next clear
                if delay and not update:                # delays clear
                    display.update()
                    sleep(self.delay)
                
            if not delay and not update:
                display.update()
            self.drawn = False              # marks that graph is not drawn

    # moves the graph by dx and dy
    def move(self, dx, dy):
        if self.drawn:
            self.draw(self.old_x + dx, self.old_y + dy, self.colour, update = True)



#=====================================================
# main program
#=====================================================

try:
    # finding distributions
    secondaryDists = []
    remlist = []
    primaryDists = PRIMARIES()
  
    if directory:
        path = directory + "."
    else:
        path = "."

    for filename in os.listdir(path):
        filename = filename.strip()
        if filename[-5:] == ".dist":
            if "&" in filename:
                secondaryDists.append(SECONDARY_DIST(filename, directory))
            else:
                primaryDists.add(PRIMARY_DIST(filename, directory))

    # associates primary distributions with secondary distributions
    if primaryDists:
        for pD in primaryDists:
            for sD in secondaryDists:
                if pD.getName() == sD.getPrimary():
                    pD.addSecondary(sD)
                    if sD not in remlist:
                        remlist.append(sD)
    
    for d in remlist:
        if d in secondaryDists:
            secondaryDists.remove(d)
    
    for sD in secondaryDists:
        primaryDists.add(PRIMARY_DIST(sD.getFilename()))   

    if not primaryDists:
        raise "No Distributions Found"

    # initializing display    
    display.set_caption("Distribution Demo:")
    window = display.set_mode((WINDOW_SIZE_X,WINDOW_SIZE_Y))
    font1 = font.Font(None, 20)
    font2 = font.Font(None, 18)
    font3 = font.Font(None, 40)
  

    key.set_repeat(1, 60)
    run = True
    
    display.update()            # updates screen


    # building graph    
    dist_factory = Cumulative.build()
    normal = dist_factory.create_dist(size, start, end)
    old_dist = normal.dist
    graph = Bar_Graph(normal.dist)    # graph of the sample

    draw.rect(window,B_COLOUR,(0, 0, WINDOW_SIZE_X, WINDOW_SIZE_Y))
    text3 = font3.render("Distribution/Analogy Demo", 1, F_COLOUR)
    window.blit(text3, (210,10))         # draws the intro text    
    
    graph.draw()                        # draws intro display
    graph.clear()                       # clears intro display
    
    DELAY_ALLOWED = False
    
    text1 = font1.render("d: draw,  c: clear,  up/down: change distribution series,  right/left: change dist, m: menu options", 1, lblue)
    window.blit(text1, (20,50))         # draws the intructions text
    temp=primaryDists.getPrevious().getCurrent()
    print temp
    graph.update_values(*temp)
    graph.draw(graph.old_x, graph.old_y)
    display.update()
    check_key = True
    
    
    # main loop
    while run:
        
        action = event.poll()               # gets keys pressed
        if action.type == KEYUP:
            check_key = True
            
        elif action.type == KEYDOWN and check_key:
            check_key = False
            # exit on next loop
            if action.key == K_ESCAPE:      
                run = False
                
            # drawns graph
            if action.key == K_d:
                graph.draw()
                event.clear()

            # clears graph
            if action.key == K_c:
                graph.clear()
                event.clear()
                
            # changes primary distribution
            if action.key == K_UP:
                graph.clear()
                graph.update_values(*primaryDists.getPrevious().getCurrent())
                graph.draw(graph.old_x, graph.old_y)
                event.clear()

            # changes primary distribution
            if action.key == K_DOWN:                
                graph.clear()
                graph.update_values(*primaryDists.getNext().getCurrent())
                graph.draw(graph.old_x, graph.old_y)
                event.clear()

            # changes secondary distribution    
            if action.key == K_LEFT:
                graph.clear()
                graph.update_values(*primaryDists.getCurrent().getPrevious())
                graph.draw(graph.old_x, graph.old_y)
                event.clear()

            # changes secondary distribution
            if action.key == K_RIGHT:                
                graph.clear()
                graph.update_values(*primaryDists.getCurrent().getNext())
                graph.draw(graph.old_x, graph.old_y)
                event.clear()


            # prints menu options
            if action.key == K_m:      
                
                event.clear()
                print "Options"
                print " >> 'help' for commands "
                print " >> 'return' to go back"
                loop = True

                while loop:
                    # gets user input
                    st = raw_input("\nprompt >> ").strip()

                    # builds a new distribution
                    if st == "new":
                        print "Note: old graph is lost"
                        size = raw_input("new size: ").strip()
                        size = int(size)
                        start = float(raw_input("Start (in Std Dev): ").strip())
                        end   = float(raw_input("End (in Std Dev): ").strip())
                        graph.clear()
                        normal = dist_factory.create_dist(size,start, end)
                        graph = Bar_Graph(normal.dist)
                        graph.draw(DEFAULT_X, DEFAULT_Y)
                        old_dist = normal.dist

                    # whether there should be a delay on redraw
                    elif st == "delay":
                        DELAY_ALLOWED = not DELAY_ALLOWED
                        print "\nDELAY_ALLOWED = " + str(DELAY_ALLOWED)

                    # undoes las change
                    elif st == "undo":
                        graph.clear()
                        graph.update_values(old_dist)
                        graph.draw(graph.old_x, graph.old_y)

                    # loads a distribution
                    elif st == "load":
                        filename = raw_input("\nFileName >> ").strip()
                        #if directory not in filename:
                        #    filename = directory + filename                        
                        new_dist = extract_distribution(filename)
                        graph.clear()
                        graph.update_values(new_dist)
                        graph.draw(graph.old_x, graph.old_y)
                        
                    # clears distribution
                    elif st == "restart":
                        graph.clear()
                        normal = dist_factory.create_dist(size)
                        graph.draw(graph.old_x, graph.old_y)

                    # writes distribution to file
                    elif st == "save":
                        filename = raw_input("\nFileName >> ").strip()
                        if filename == "":
                            filename = "output.txt"
                        print '\ndistribution written to "' + filename + '"'
                        FILE = open(filename, "w")  
                        for v in graph.values:
                            FILE.write(str(v) + "\n")
                        FILE.close()

                    # returns to main window
                    elif st == "return":
                        loop = False

                    # exits program
                    elif st == "exit":
                        loop = False
                        run = False

                    # prints options menu
                    elif st == "help" or st == "/?" or st == "-?":
                        print "COMMAND  - DESCRIPTION"
                        print "----------------------"
                        print "new      - creates a new distribution"
                        print "load     - loads distribution from a file"
                        print "delay    - toggles whether delay is allowed"
                        print "undo     - undoes last modification"
                        print "restart  - resets distribution"
                        print "return   - returns to the other screen"
                        print "save     - saves distribution to output.txt"
                        print "exit     - exits program"
                        print
                        print "Non-command expressions are evaluated by the interpreter"

                    else:
                        # checks for systax error exceptions
                        try:
                            normal.dist = graph.values
                            old_dist = normal.dist
                            exec st
                            if graph.values != normal.dist or st == "normal.reverse()":
                                graph.clear()
                                graph.update_values(normal.dist)
                                graph.draw(graph.old_x, graph.old_y)
                            
                        except Exception, extraInfo:
                            print "\n", extraInfo

                    
        # exits loop
        if action.type == QUIT:
            run = False

    
finally:
    display.quit()  # removes display


