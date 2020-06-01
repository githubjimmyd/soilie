#######################################################################
#
# probability.py
# ---------------
#
# Description:  Contains information pertaining to normal distributions 
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
from math import *


# holds the discrete cumulative distribution for a standard normal distribution
class Cumulative:

    @staticmethod
    def build():

        d = Cumulative()
        d.initialize()
        return d

    def initialize(self):

        self.dist = []                          # table holding the discrete cumulative distribution
        self.filename = "CumulativeDist.txt"    # name of file storing the distribution values
        self.interval = 0.01                    # interval of the discrete distribution
        
        # opens the file for reading
        FILE = open(self.filename, "r")  

        # reads each line of the file one by one
        for line in FILE:
            self.extract_floats(line)

        FILE.close()
        

    # read the cumulative distribution values from a file
    # and addes them to the distribution table
    def extract_floats(self, string):
        if len(string) == 0:
            return
        else:
            if string.find(" ") == -1:
                self.dist.append(float(string))
                return
            else:
                self.dist.append(float(string[0:string.find(" ")]))
                self.extract_floats(string[string.find(" ")+1:])    



    # interpolates to find any value of the cumulative distribution
    def get_stn_dist(self, z):
        # case where z is negative
        if z < 0:
            z *= -1
            neg_flag = -1
        # case where z is positive
        else:
            neg_flag = 1
            
        z /= self.interval
        zInt = int(z)
        zDif = z - zInt
        maxZ = len(self.dist)-1          # max element in distribution

        # case where z is within table
        if z < maxZ:
            dist_value = self.dist[zInt]*(1-zDif) + self.dist[zInt+1]*zDif
        # case where z is larger then the table
        else:
            dist_value = 0.5

        return dist_value*neg_flag + 0.5

    # calculates the cumulative distribution between two values
    def calc_dist(self, x1, x2, mean = 0, std_dev = 1):
        z1 = (x1 - mean)/sqrt(std_dev)
        z2 = (x2 - mean)/sqrt(std_dev)
        return self.get_stn_dist(z2) - self.get_stn_dist(z1)

    # creates a discrete normal distribution 
    def create_dist(self, num, start = -3, end = 3, mean = 0, std_dev = 1):
        # num in the number of values in the distribution
        # start is the beginning of the dist. in std_dev(s) units 
        # end is the ending of the dist. in std_dev(s) units
        # -1 to 1  -> 68%
        # -2 to 2  -> 95%
        # -3 to 3  -> 99.7%
        
        dist = []
        interval = (end - start)/num
        position = start
        
        while(num > 0):
            dist.append(self.calc_dist(position, position+interval, mean, std_dev))
            position += interval
            num -= 1

        return Distribution(dist, interval)
        
class Distribution:

    def __init__(self, dist, interval=0.01):
        self.dist = dist
        self.interval = interval


    # normalizes the distribution (i.e. makes the total equal to one)
    def normalize(self):
        total = 0           
        for d in self.dist:         # calculates the summation
            total += d
        mod = 1/total               # determines how much to modify the sequence by
        temp = []                   # stores the new dist.
        for d in self.dist:         # modifies each element
            temp.append(d*mod)
        self.dist = temp            

    # reverses the distribution
    def reverse(self):
        self.dist.reverse()

    # transforms the values of the distribution
    def transform(self, function, start=1, end=1):
        temp = []                       # temporary storage
        length = len(self.dist)
        if length >= 1:
            length -= 1
        change = (end-start)/length
        for d in self.dist:             # transforms each element according to 'function'
            temp.append(function(d, start))
            start += change
        self.dist = temp

    # modifies the distribution such that the apex is equal to 'max' and the 
    def stretch(self, maximum = "Same", minimum = "Same"):        
        if len(self.dist) < 1:
            return
        minV = self.dist[0]
        maxV = self.dist[0]
        for d in self.dist:
            if d > maxV:
                maxV = d
            if d < minV:
                minV = d
        if maximum == "Same":
            maximum = maxV
        if minimum == "Same":
            minimum = minV
        mod = (maximum-minimum)/(maxV-minV)     # determines how much to modify the sequence by
        temp = []                   # stores the new dist.
        for d in self.dist:         # modifies each element
            temp.append((d-minV)*mod + minimum)
        self.dist = temp            

    def flip(self):
        minV = self.dist[0]
        maxV = self.dist[0]
        for d in self.dist:
            if d > maxV:
                maxV = d
            if d < minV:
                minV = d
        self.transform(lambda x, y: (x*(-1) + minV + maxV) )

    def inverse(self):
        self.transform(lambda x, y: x*(-1))
            
    # returns the string representation
    def __str__(self):
        return "Interval: " + str(self.interval) + "\n" + str(self.dist)
    

# --- example
if __name__ == "__main__":
    
    dist_factory = Cumulative.build()
    normal = dist_factory.create_dist(5)
    print "Normal distribution"
    print normal
    print
    normal.normalize()
    print "After normalization"
    print normal
    print
    normal.flip()
    print "After flipped"
    print normal
    print
    normal.stretch(2, -1)
    print "After stretched: Max 2, min -1"
    print normal
    print
