###############################################################################
#
# distribution_demo.py
# ---------------------
#
# Description: Demos the distribution modifier and concept creation system
#
# Author:   Jonathan Gagne
#           Institute of Cognitive Science
#           Carleton University
#           jgagne2@connect.carleton.ca
#
# For:      Undergraduate Thesis
# Supervisor: Dr. Jim Davies
#
###############################################################################

DEMO = [4]                  # list of demos to run
WRITE_FILES = True          # whether examples should be written


from distance import *
from angle import *
from modifier import *



if 1 in DEMO:
    
    line1 = DISTANCE()
    line2 = DISTANCE()
    line3 = DISTANCE()
    
    for i in xrange(1,20):
        line1.fuzzify(i*50)
            
    line2.fuzzify(500)
    line2.fuzzify(700)
    line2.fuzzify(900)
        
    #line1.output()
    #line2.output()
    line3.degrees_of_membership = line1.degrees_of_membership[3:]
    line3.degrees_of_membership.append(0.0)
    line3.degrees_of_membership.append(0.0)
    line3.degrees_of_membership.append(0.0)
    #line3.output()
        
    line2.get_modifier(line1)
        
    lineX = MODIFIER.modify(line2.get_modifier(line1), line3)
        
    lineX.output()
    
    if WRITE_FILES:
        line1.write_membership_distribution("Lions.dist", "All Lions")
        line2.write_membership_distribution("Lions&Big.dist", "Only Big Lions")
        line3.write_membership_distribution("Dogs.dist", "All Dogs")
        lineX.write_membership_distribution("Dogs&Big.dist", "Only Big Dogs (Estimated)")

    
    
    #-------------

if 2 in DEMO:
    
    width = DISTANCE()
    #widthBig = DISTANCE()
    height = DISTANCE()
    heightSmall = DISTANCE()
    heightMedium = DISTANCE()
    heightBig = DISTANCE()
    
    height.set_membership_from_distibution_file(r"dist_demo\height.dist")
    heightSmall.set_membership_from_distibution_file("dist_demo\height&small.dist")
    heightMedium.set_membership_from_distibution_file("dist_demo\height&medium.dist")
    heightBig.set_membership_from_distibution_file("dist_demo\height&big.dist")
    
    width.set_membership_from_distibution_file(r"dist_demo\width.dist")
    
    height.output()
    heightSmall.output()
    heightMedium.output()
    heightBig.output()
    width.output()
    #widthBig.output()
    heightSmall_mod = heightSmall.get_modifier(height)
    heightMedium_mod = heightMedium.get_modifier(height)
    heightBig_mod = heightBig.get_modifier(height)
    #print height_mod
    widthSmall = MODIFIER.modify(heightSmall_mod, width)
    widthMedium = MODIFIER.modify(heightMedium_mod, width)
    widthBig = MODIFIER.modify(heightBig_mod, width)
    
    
    if WRITE_FILES:    
        widthSmall.write_membership_distribution("width&small.dist", "small width (Estimated)")
        widthMedium.write_membership_distribution("width&medium.dist", "medium width (Estimated)")
        widthBig.write_membership_distribution("width&big.dist", "big width (Estimated)")


if 3 in DEMO:
    
    vertical = ANGLE()
    verticalVery = ANGLE()
    horizontal = ANGLE()
    
    vertical.set_membership_from_distibution_file(r"dist_demo\vertical.dist")
    verticalVery.set_membership_from_distibution_file(r"dist_demo\vertical&very.dist")
    horizontal.set_membership_from_distibution_file(r"dist_demo\horizontal.dist")
    
    verticalVery_mod = verticalVery.get_modifier(vertical)
    print verticalVery_mod
    horizontalVery = MODIFIER.modify(verticalVery_mod, horizontal)
    
    if WRITE_FILES:
        horizontalVery.write_membership_distribution("horizontal&very", "very horizontal (estimated)")
        
if 4 in DEMO:
    
    crow = DISTANCE()
    crowLarge = DISTANCE()
    raven = DISTANCE()
        
    crow.set_membership_from_distibution_file(r"dist_demo\Crows.dist")
    crowLarge.set_membership_from_distibution_file(r"dist_demo\Crows&Large.dist")
    raven.set_membership_from_distibution_file(r"dist_demo\Ravens.dist")
        
    crowLarge_mod = crowLarge.get_modifier(crow)
    ravenLarge = MODIFIER.modify(crowLarge_mod, raven)
    
    
    if WRITE_FILES:
        ravenLarge.write_membership_distribution("Ravens&Large.dist", "Large Ravens (estimated)")
        

from dist_graph_demo import * 

