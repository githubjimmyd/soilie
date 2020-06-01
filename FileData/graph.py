#######################################################################
#
# graph.py
# --------
#
# Description:  Creates distributions 
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
from angle import *
from distance import *


# initializing imports
display.init()
font.init()

DEFAULT_SIZE = 15       # default distribution size
DEFAULT_START = -3      # default starting standard deviations
DEFAULT_END = 3         # default ending standard deviations

B_COLOUR = black    # background colour

WINDOW_SIZE_X = 800     # X size of window
WINDOW_SIZE_Y = 600     # Y size of window

DEFAULT_X = 20          # default x position of graph
DEFAULT_Y = 350         # default y position of graph

sep = 2                 # separation of bars

DEFAULT_DELAY = 1.0     # delay of bar display
DELAY_ALLOWED = True    # whether delay is allowed
scale = 1.05


# bar graph of a list
class Bar_Graph:
    
    # constructor
    def __init__(self, graph_list, title='', X_AXIS_VALS=[], sizeX = 600, sizeY = 200, print_values = True):
        self.values = graph_list            # the heights of the bar graph are taken from the list
        self.sizeX = sizeX                  # width of the bars
        self.sizeY = sizeY                  # height of the bars (muliplied by values)
        self.print_values = print_values    # whether the values should be printed (not implemented)
        self.delay = DEFAULT_DELAY          # draw delay in seconds
        if X_AXIS_VALS:
            self.X_AXIS_VALS = X_AXIS_VALS
        else:
            self.X_AXIS_VALS = range(len(self.values))
        self.title = title

               
        self.maxValue = max(self.values)    # gets max height
        self.minValue = min(self.values)    # gets min height
        self.maxAbsVal = max([self.maxValue, -self.minValue])
        
        if self.maxAbsVal == 0:
            self.maxAbsVal = 1
        self.old_maxAbsVal = self.maxAbsVal

        self.drawn = False                  # whether the graph is currently drawn
        
        self.old_values = []                # old values to be erased (used for clear)
        self.old_sizeX = self.sizeX         # old width (used for clear)
        self.old_sizeY = self.sizeY         # old height (used for clear)
        self.old_x = 0                     # old x location of graph (used for clear)
        self.old_y = 0                     # old y location of graph (used for clear)
        self.old_print_values = print_values    # old print of values option (used for clear)
        

    # updates graph values
    def update_values(self, graph_list):
        self.values = graph_list
        
    def update_value(self, val, index):
        self.values[index] = val

    def update_max_value(self):
        self.old_maxAbsVal = self.maxAbsVal
        
        self.maxValue = max(self.values)    # gets max height
        self.minValue = min(self.values)    # gets min height
        self.maxAbsVal = max([self.maxValue, -self.minValue])
        
        if self.maxAbsVal == 0:
            self.maxAbsVal = 1

    # draws the graph onto the screen at x, y.        
    def draw(self, x=DEFAULT_X, y=DEFAULT_Y, colour = white, delay = True, update = False):

        if not DELAY_ALLOWED:
            delay = False

        self.update_max_value()
        
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
        
        xpos = x                    # position marker for x
        length = len(self.values)
        draw.rect(window,dblue,(xpos-1, y-self.sizeY-1, self.sizeX+sep*length+2, 2*self.sizeY+2))
        # draws each bar one by one
        for val,xVal in zip(self.values,self.X_AXIS_VALS):
            #draw.rect(window,blue,(xpos+5,y-self.sizeY,self.sizeX//length-10,2*self.sizeY+1))
            draw.rect(window,colour,(xpos,y-(val/self.maxAbsVal)*self.sizeY,self.sizeX//length,(val/self.maxAbsVal)*self.sizeY+1))            
            text_val = transform.rotate(font2.render("%.5f" % val, True, lred), 270)
            x_val = transform.rotate(font2.render(str(xVal)+"   ", True, white, B_COLOUR), 270)
            if self.print_values:
                if val < 0:
                    mod = -60
                else:
                    mod = 10
                window.blit(text_val, (xpos+(self.old_sizeX//length)/2-8,self.old_y+mod))     # draws the value under bar
                window.blit(x_val,(xpos+(self.old_sizeX//length)/2-8,self.old_y-40-self.old_sizeY))           # draws x-axis val           
            
            xpos = xpos + self.sizeX//length + sep        # sets position for next bar
            
            if delay and not update:                           # delays draw
                display.update()
                sleep(self.delay/size)

        if not delay or update:
            display.update()
        
    # clears the bar graph (redraws with black as default)
    def clear(self, colour = B_COLOUR, delay = True, update = False):

        if not DELAY_ALLOWED:
            delay = False

        self.update_max_value()

        length = len(self.values)

        # clears if graph is drawn
        if self.drawn:
            xpos = self.old_x               # x position marker
            # clears each bar
            for val,xVal in zip(self.old_values,self.X_AXIS_VALS):
                draw.rect(window,colour,(xpos, self.old_y-(val/self.old_maxAbsVal)*self.old_sizeY, self.old_sizeX//length, (val/self.old_maxAbsVal)*self.old_sizeY+1))
                text_val = transform.rotate(font2.render("%.5f" % val, True, colour, B_COLOUR), 270)
                x_val = transform.rotate(font2.render(str(xVal)+"   ", True, colour, B_COLOUR), 270)                
                if val < 0:
                    mod = -55
                else:
                    mod = 10
                window.blit(text_val, (xpos+(self.sizeX//length)/2-8,self.old_y+mod))     # draws the value under bar
                window.blit(x_val, (xpos+(self.sizeX//length)/2-8,self.old_y-40-self.sizeY))         # draws x-axis val
            
                xpos = xpos + self.old_sizeX//length + 3        # increases position marker for next clear
                if delay and not update:                # delays clear
                    display.update()
                    sleep(self.delay/size)
                
            if not delay and not update:
                display.update()
            self.drawn = False              # marks that graph is not drawn

    # moves the graph by dx and dy
    def move(self, dx, dy):
        if self.drawn:
            self.draw(self.old_x + dx, self.old_y + dy, self.colour, update = True)


    
    



#===============================================================================
# Main Program
#===============================================================================
if __name__ == "__main__":
    try:
        
        # new or load
        val = raw_input("(n)ew or (l)oad: ").strip().lower()
        if val == "load": val = 'l'
        elif val == "new": val = 'n'
        elif val != 'n' and val != 'l': 
            val = 'n'
            print "Not recognised -- Creating new"
            
        if val == 'n':        
            
            # gets size of distribution
            val = raw_input("Size of distribution: ").strip()
            if val:
                size = int(val)
            else:
                size = DEFAULT_SIZE
                print "  using default size:",size
        
            # gets left size standard deviation (default -3)
            val = raw_input("Start (in Std Dev): ").strip()
            if val:
                start = float(val)
            else:
                start = DEFAULT_START
                print "  using default start:",start
            
            # gets left size standard deviation (default 3)
            val = raw_input("End (in Std Dev):  ").strip()
            if val:
                end = float(val)
            else:
                end = DEFAULT_END
                print " using default end:",end
                
            # Gets the x-axis metric
            val = raw_input("X-axis Values (distance/angle/custom/default):  ").strip().lower()
            if val == 'distance':
                xAxisVals = DISTANCE.qualitative_values[:]
            elif val == 'angle':
                xAxisVals = ANGLE.qualitative_values[:]
            elif val == 'custom':
                xAxisVals = []
                print "Enter each value and hit enter. Enter", str(size),"values."                
                for i in xrange(size):
                    val = float(raw_input().strip())
                    xAxisVals.append(val)                
            else:
                xAxisVals = range(size)
                print " using default: ",xAxisVals
               
                
        
            dist_factory = Cumulative.build()
            normal = dist_factory.create_dist(size, start, end)
            old_dist = normal.dist
            graph = Bar_Graph(normal.dist,title='',X_AXIS_VALS=xAxisVals)    # graph of the sample
        
        
        else:
            filename = raw_input("\nFileName >> ").strip()
            if filename[-5:] != ".dist":
                filename = filename + ".dist"
            load_dist, extra_info = extract_distribution(filename, extra_info=True)
            title = ''
            size = len(load_dist)
            xAxisVals = range(size)
            for info in extra_info:
                try:
                    exec(info)
                except Exception, val:
                    print "Invalid Extra Info: " + str(val)
            old_dist = load_dist
            normal = Distribution(load_dist)
            graph = Bar_Graph(load_dist,title=title,X_AXIS_VALS=xAxisVals)    # graph of the sample
            
        
        # initialization
        display.set_caption("Graphs and Modifies Normal distributions")
        window = display.set_mode((WINDOW_SIZE_X,WINDOW_SIZE_Y))
        font1 = font.Font(None, 20)
        font2 = font.Font(None, 18)
        text1 = font2.render("Draw: d,  Clear: c,  Menu: m,  Shift Dist.: Left/Right Arrows,  Scale all values: Up/Down Arrows", 1, lgrey)
        text2 = font2.render("Mouse Buttons -> Left: set value,  Right: remove value,  Wheel: scale value", 1, lgrey)
        
        key.set_repeat(1, 60)
        run = True          
    
        window.blit(text1, (20,20)) # draws the text
        window.blit(text2, (20,35)) # draws the text
        display.update()            # updates screen
        

        graph.draw()
    
        # main loop
        while run:
            
            # gets keys pressed
            action = event.poll()
            
            # check if a mouse button is clicked
            if action.type == MOUSEBUTTONDOWN:
                
                # if left mouse button -> set value to clicked size
                if action.button == 1:
                    mouseX, mouseY = mouse.get_pos()
                    graph.update_max_value()    
                    xpos = DEFAULT_X                    # position marker for x
                    y = DEFAULT_Y
                    length = len(graph.values)
                    # draws each bar one by one
                    for i in xrange(length):                    
                        if (mouseX > xpos) and (mouseY > y-graph.sizeY) and (mouseX < xpos+graph.sizeX//length) and (mouseY < y+graph.sizeY+1):
                            val = ((y - mouseY)/graph.sizeY) * graph.maxAbsVal
                            graph.update_value(val,i)
                            graph.draw(update=True)
                            break                                      
                        xpos = xpos + graph.sizeX//length + 3        # sets position for next bar
                        
                # if right mouse button -> clear value at location
                elif action.button == 3:
                    mouseX, mouseY = mouse.get_pos()                       
                    graph.update_max_value()
                    xpos = DEFAULT_X                    # position marker for x
                    y = DEFAULT_Y
                    length = len(graph.values)
                    # draws each bar one by one
                    for i in xrange(length):                    
                        if (mouseX > xpos) and (mouseY > y-graph.sizeY) and (mouseX < xpos+graph.sizeX//length) and (mouseY < y+graph.sizeY+1):
                            val = 0
                            graph.update_value(val,i)
                            graph.draw(update=True)
                            break                                        
                        xpos = xpos + graph.sizeX//length + 3        # sets position for next bar
                
                # if mouse scroll up -> increase chosen value
                elif action.button == 4:
                    mouseX, mouseY = mouse.get_pos()                           
                    graph.update_max_value()
                    xpos = DEFAULT_X                    # position marker for x
                    y = DEFAULT_Y
                    length = len(graph.values)
                    # draws each bar one by one
                    for i in xrange(length):                    
                        if (mouseX > xpos) and (mouseY > y-graph.sizeY) and (mouseX < xpos+graph.sizeX//length) and (mouseY < y+graph.sizeY+1):
                            val = graph.values[i] + graph.maxAbsVal/20
                            graph.update_value(val,i)
                            graph.draw(update=True)
                            break                                        
                        xpos = xpos + graph.sizeX//length + 3        # sets position for next bar
                
                # if mouse scroll down -> decrease chosen value
                elif action.button == 5:
                    mouseX, mouseY = mouse.get_pos()                         
                    graph.update_max_value() 
                    xpos = DEFAULT_X                    # position marker for x
                    y = DEFAULT_Y
                    length = len(graph.values)
                    # draws each bar one by one
                    for i in xrange(length):                    
                        if (mouseX > xpos) and (mouseY > y-graph.sizeY) and (mouseX < xpos+graph.sizeX//length) and (mouseY < y+graph.sizeY+1):
                            val = graph.values[i] - graph.maxAbsVal/20
                            graph.update_value(val,i)
                            graph.draw(update=True)
                            break                                        
                        xpos = xpos + graph.sizeX//length + 3        # sets position for next bar
            
            
            # checks if a key is pressed
            elif action.type == KEYDOWN:
    
                # exit on next loop
                if action.key == K_ESCAPE:      
                    run = False
                    
                # draws graph
                if action.key == K_d:
                    graph.draw()
                    event.clear()
    
                # clears graph
                if action.key == K_c:
                    graph.clear()
                    event.clear()
                    
                # increases distribution values
                if action.key == K_UP:
                    temp = []                   # stores the new dist.
                    for d in graph.values:      # modifies each element
                        temp.append(d*scale)
                    graph.values = temp
                    graph.move(0,0)
                    
                # decreases distribution values
                if action.key == K_DOWN:
                    temp = []                   # stores the new dist.
                    for d in graph.values:      # modifies each element
                        temp.append(d/scale)
                    graph.values = temp                
                    graph.move(0,0)
                    
                # shifts distribution to the left
                if action.key == K_LEFT:
                    graph.values.append(graph.values[0])
                    graph.values = graph.values[1:]
                    graph.move(0,0)
                    event.clear()
                
                # shifts distribution to the right        
                if action.key == K_RIGHT:                
                    graph.values.insert(0, graph.values.pop(len(graph.values)-1))
                    graph.move(0,0)
                    event.clear()
                    
                # clears graph
                if action.key == K_m:      
                    
                    event.clear()
                    print "Modify distribution"
                    print " >> 'help' for commands "
                    print " >> 'return' to go back"
                    loop = True
    
                    while loop:
                        st = raw_input("\nprompt >> ").strip()
                        if st == "new":
                            print "Note: old graph is lost"
                            size = raw_input("new size: ")
                            size = int(size)
                            start = float(raw_input("Start (in Std Dev): "))
                            end   = float(raw_input("End (in Std Dev): "))
                            graph.clear()
                            normal = dist_factory.create_dist(size,start, end)
                            graph = Bar_Graph(normal.dist)
                            graph.draw(DEFAULT_X, DEFAULT_Y)
                            old_dist = normal.dist
    
                        elif st == "delay":
                            global DELAY_ALLOWED
                            DELAY_ALLOWED = not DELAY_ALLOWED
                            print "\nDELAY_ALLOWED = " + str(DELAY_ALLOWED)
                        
                        elif st == "undo":
                            normal = Distribution(old_dist)
                            graph.clear()
                            graph.update_values(old_dist)
                            graph.draw(graph.old_x, graph.old_y)
    
                        elif st == "load":
                            filename = raw_input("\nFileName >> ").strip()
                            if filename[-5:] != ".dist":
                                filename = filename + ".dist"
                            load_dist = extract_distribution(filename)
                            normal = Distribution(load_dist)
                            graph.clear()
                            graph.update_values(load_dist)
                            graph.draw(graph.old_x, graph.old_y)
                            
    
                        elif st == "restart":
                            graph.clear()
                            normal = dist_factory.create_dist(size)
                            graph.draw(graph.old_x, graph.old_y)
    
                        elif st == "save":
                            filename = raw_input("\nFileName >> ").strip()
                            title = raw_input("\nTitle >> ").strip()
                            if filename == "":
                                filename = "output.dist"
                            elif filename[-5:] != ".dist":
                                filename = filename + ".dist"
                            print '\ndistribution written to "' + filename + '"'
                            FILE = open(filename, "w")
                            if title == "":
                                title = filename[:-5]  
                            FILE.write('title="' + title + '"\n')
                            FILE.write("xAxisVals=" + str(graph.X_AXIS_VALS))
                            FILE.write("\n")
                            for v in graph.values:
                                FILE.write(str(v) + "\n")
                            FILE.close()
    
                        elif st == "return":
                            loop = False
    
                        elif st == "exit":
                            loop = False
                            run = False
    
                        elif st == "help" or st == "/?" or st == "-?":
                            print "COMMAND  - DESCRIPTION"
                            print "----------------------"
                            print "new      - creates a new distribution"
                            print "load     - loads distribution from a file"
                            print "delay    - toggles whether delay is allowed"
                            print "undo     - undoes last modification"
                            print "restart  - resets distribution"
                            print "return   - returns to the other screen"
                            print "save     - writes distribution to file"
                            print "exit     - exits program"
                            print
                            print "* note: to make transformations type in 'normal.<function>'"
                            print "        where <function> is one of the ones below"
                            print "             normalize()"
                            print "             reverse()"
                            print "             strech([max [, min])"
                            print "             flip()"
                            print "             inverse()"
                            print "             transform(func [, start [,stop]])"
                            print
                            print "Non-command expressions are evaluated by the interpreter"
                            print
    
                        else:
                            # checks for syntax error exceptions
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
    
    
    
