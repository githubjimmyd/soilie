import subprocess
import sys
import time

def isAllDone(processes):
    done = 0
    for process in processes:
        if (process.poll() == 0):
            done += 1
    if done == len(processes):
        return True
    else:
        return False

def main():
	numberOfFile = 1
	for i in range(1, 318):#Runs files 1 through 1267
		number = 4
		if len(sys.argv) > 1:
			number = eval(sys.argv[1])
		processes = []
		for i in range(number):
			if numberOfFile == 1268:
				break
			else:
				processes.append(subprocess.Popen([sys.executable,"sim2_NotSavingExemplar.py", str(numberOfFile)]))
				numberOfFile = numberOfFile+1



		alldone = False
		while not alldone:
			alldone = isAllDone(processes)
			time.sleep(10)
        print "Done"
    	print numberOfFile

if __name__=="__main__":
    main()