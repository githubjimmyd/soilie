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
	numberOfFile = 1268
	for i in range(1, 319):#Runs files 1268 to 1902 (634 files, 1/3 of total)
		number = 2
		if len(sys.argv) > 1:
			number = eval(sys.argv[1])
		processes = []
		for y in range(number):
			if numberOfFile == 1903:
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