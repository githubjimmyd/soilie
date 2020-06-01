#######################################################################
#
# link.py
# -------
#
# Description:  Holds three types of links, which are objects used  
#               to connect concepts together such that they can
#               communicate.
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


#------------------------------------
# basic link
class LINK:
    def __init__(self, target, capability):
        self.target = target                # target of the link
        self.name = ID.generate(self)       # name of the link
        self.codeFilter = []                # stores the code that acts as a filter to concepts that are sent by the link
        self.capability = capability        # type of link (eg. EXCITABLE)

    # sends an activation to the target concept
    def send(self, signal):
        # runs filter code
        for code in self.codeFilter:
            exec(code)
            
        # sends signal
        self.target.receive(signal, self.capability)
        

    # sets any code to be initialized (ie, ran once)
    # syntax:   init_code('code_string1' [,'code_string2' [,'code_string3,' [, etc]]])
    # eg:       init_code('self.strength = 0.8', 'self.decay = 0.9')
    def init_code(self, *args):
        for code in args:
            exec(code)

    # sets the filter code (ie, ran each time a signal is transmitted)
    # code should modify the 'signal' parameter sent to the 'send' method
    # syntax:   filter_code('code_string1' [,'code_string2' [,'code_string3,' [, etc]]])
    # eg:       filter_code('signal *= self.strength')
    def filter_code(self, *args):
        self.codeFilter = []
        for code in args:
            self.codeFilter.append(compile(code, "<string>", "exec"))
        

    # returns a representation of itself
    def __repr__(self):
        string = "Target: " + str(self.target.name) 
        return string


# represents a unidirectional connection from source to target
class LINK_UNI:
    def __init__(self, source, target):
        self.source = source                # source concept
        self.targets = target               # target concept
        self.name = ID.generate(self)       # produces unique name
        self.codeFilter = []                # stores the code that acts as a filter to concepts that are sent by the link

    # sends an activation to the target concept
    def send(self, command):
        # lets the command know the target
        command.set_target = self.target

        # runs code that runs command through a filter
        for code in self.codeFilter:
            exec(code)

        # sends command
        self.target.receive(command)

    # sets any code to be initialized (ie, ran once)
    # syntax:   init_code('code_string1' [,'code_string2' [,'code_string3,' [, etc]]])
    # eg:       init_code('self.strength = 0.8', 'self.decay = 0.9')
    def init_code(self, *args):
        for code in args:
            exec(code)

    # sets the filter code (ie, ran each time a signal is transmitted)
    # code should modify the command (object) parameter sent to the 'send' method
    # syntax:   filter_code('code_string1' [,'code_string2' [,'code_string3,' [, etc]]])
    # eg:       filter_code('signal *= self.strength')
    def filter_code(self, *args):
        self.codeFilter = []
        for code in args:
            self.codeFilter.append(compile(code, "<string>", "exec"))

    # returns a representation of itself
    def __repr__(self):
        string = "Unidirectional connection --- Source: " + str(self.source) + "  ->  Target: " + str(self.target)
        return string

    ## get and set methods ----------------------
    def get_source(self):
        return self.source

    def get_target(self):
        return self.target
    ## End of get and set method section --------


# represents two or more connected concepts.  
class LINK_MULTI:
    def __init__(self, targets):        
        self.targets = targets          # all connecting points of the link
        self.name = ID.generate(self)   # generates unique name
        self.codeFilter = []            # stores the code that acts as a filter to concepts that are sent by the link

    # sends command to all non-source target
    def send(self, command):
        source = command.get_source()   # determines where the concept is sent from

        # runs code that runs command through a filter
        for code in self.codeFilter:
            exec(code)

        # send the command to each non-source target
        for targ in self.targets:
            if targ != source:
                # copies command to be sent to each target
                commandcopy = command.copy()                
                # lets the command know the target
                commandcopy.set_target = self.target
                # sends command
                self.targ.receive(commandcopy)


    # sets any code to be initialized (ie, ran once)
    # syntax:   init_code('code_string1' [,'code_string2' [,'code_string3,' [, etc]]])
    # eg:       init_code('self.strength = 0.8', 'self.decay = 0.9')
    def init_code(self, *args):
        for code in args:
            exec(code)

    # sets the filter code (ie, ran each time a signal is transmitted)
    # code should modify the command (object) parameter sent to the 'send' method
    # syntax:   filter_code('code_string1' [,'code_string2' [,'code_string3,' [, etc]]])
    # eg:       filter_code('signal *= self.strength')
    def filter_code(self, *args):
        self.codeFilter = []
        for code in args:
            self.codeFilter.append(compile(code, "<string>", "exec"))

    # returns a representation of itself
    def __repr__(self):
        string = "Target : " + str(self.targets)
        return string

    ## Get and Set methods --------------
    def get_targets(self):
        return self.targets
    ## End: Get and set methods ---------


from ID import *
