# counts the programs lines of codes
import os
i = 0
for filename in os.listdir("."):
    if filename[-3:] == ".py":   
        f = open(filename.strip())
        for line in f.xreadlines():
            i += 1
print "Lines of code: ", i