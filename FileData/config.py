#######################################################################
#
# config.py
# ---------
#
# Description: loads program configurations from settings.txt  
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


# initializes program options from options.txt

class config:
    options = []
    init = False
    
    @staticmethod
    def isinitialized():
        return config.init
        
if not config.init:
    f = open("settings.txt")
    for line in f.xreadlines():
        if "#" in line:
            line = line[0:line.find("#")]
        line = line.strip()
        
        if line:
#            if "pyg_vars." in line:
#                exec(line)
#            else:                
#                exec("config." + line)
            exec("config." + line)
        
    config.init = True
else:
    raise "config class initialized twice"





