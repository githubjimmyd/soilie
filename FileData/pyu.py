import subprocess
import random
import OracleScript2
import sys
import displayImagenet as display
from Thesis_fix_pyu_old import Coherencer
#from visuobeta import VisuoBeta


c = Coherencer()
##v = VisuoBeta(db='K:\\visuodb_2015-04-25')
data_source = "image_names.txt"
image_dir = "peekaboom/images/"

oracle_threshold = 0.02
image_codes = []
code_labels = {}
number = 5

def main():
    #using_imagenet = True
    test = True
    print("Use ImageNet or Peekaboom [I/P]?")
    while test:
        query = input()
        if query == 'I' or query == 'i' or query == "ImageNet" \
           or query == "Imagenet" or query == "imageNet" or query == "imagenet":
            using_imagenet = True
            test = False
        elif query == 'P' or query == 'p' or query == "Peekaboom" \
             or query == "peekaboom":
            using_imagenet = False
            using_peekaboom = True
            test = False
        else:
            print("That is not a valid option. Please enter I or P.")

    if using_imagenet == False:
        with open(data_source, 'r') as f:
            lines = [line for line in f]
            print(len(lines))
            for i in range(len(lines)):
##                print(lines[i])
##                print("-------------------------")
##                print("-------------------------")
##                print("-------------------------")
                line_split = lines[i].split(':')
                image_codes.append(line_split[0])
                label_split = line_split[1].split(',')
                #print(len(label_split))
                code_labels[line_split[0]] = label_split
            
            
        
            
    test = True
    print("Use Oracle or Coherencer [O/C]?")
    while test:
        query = input()
        if query == 'O' or query == 'o' or query == 'Oracle' \
           or query == 'oracle':
            using_oracle = True
            test = False
        elif query == 'C' or query == 'c' or query == 'Coherencer' \
            or query == 'coherencer':
            using_oracle = False
            print("Please pick degree of coherence:")
            print("weak, moderate, or strict [W/M/S]?")
            while test:
                query = input()
                if query == 'W' or query == 'w' or query == 'weak' \
                   or query == 'Weak':
                    threshold = 0.1
                    test = False
                elif query == 'M' or query == 'm' or query == 'moderate' \
                    or query == 'Moderate':
                    threshold = 0.3
                    test = False
                elif query == 'S' or query == 's' or query == 'strict' \
                        or query == 'Strict':
                    threshold = 0.5
                    test = False
                else:
                    print("That is not a valid option. Please enter W, M, or S.")
        else:
            print("That is not a valid option. Please enter O or C.")
    test = True
    print("Display or save image [D/S]?")
    while test:
        query = input()
        if query == 'D' or query == 'd' or query == 'Display' \
           or query == 'display':
            image_output = False
            test = False
        elif query == 'S' or query == 's' or query == 'Save' or query == 'save':
            image_output = True
            test = False
        else:
            print("That is not a valid option. Please enter D or S.")
    test = True
    print("Use background image [Y/N]?")
    while test:
        query = input()
        if query == 'Y' or query == 'y' or query == 'yes' or query == 'Yes':
            add_background = True
            test = False
        elif query == 'N' or query == 'n' or query == 'no' or query == 'No':
            add_background = False
            test = False
        else:
            print("That is not a valid option. Please enter Y or N.")
    test = True
    print("Use cut and fill [Y/N]?")
    while test:
        query = input()
        if query == 'Y' or query == 'y' or query == 'yes' or query == 'Yes':
            cut_background = True
            test = False
        elif query == 'N' or query == 'n' or query == 'no' or query == 'No':
            cut_background = False
            test = False
        else:
            print("That is not a valid option. Please enter Y or N.")
    test = True
    print("Please insert single word query.")
    while test:
        query = input()
        if using_imagenet == True:
            if query in c.db:
                test = False
            else:
                print("That query is not in the database.")
                print("Please pick another query.")
        else:
            selections = []
            for i in range(len(image_codes)):
                if query in code_labels[image_codes[i]]:
                    selections.append(image_codes[i])
            if len(selections) == 0:
                print("Matching image not found.")
                print("Please pick another query.")
            else:
                test = False
                picture = random.choice(selections)
                image_name = image_dir + picture + ".jpg"
    if using_imagenet == True:
        bracketedquery = "[" + query + "]"

        visuofile = open("FromVisuoToDisplay"+query+".txt", "w")
        visuofile.write("#" + query + "\n")
        visuofile.close()

        objects = []

        if using_oracle == True:
           oracle_answers = OracleScript2.proximity(query)
           for item in oracle_answers:
               if float(oracle_answers[item]) > oracle_threshold:
                   objects.append(((float(oracle_answers[item])),item))
        #random.shuffle(objects)
        else:
            test = True
            while test:
                objects = c.runLoop(number, query, threshold)
##        objects = objects[1:]
                print(objects)
                print("Is this selection good?")
                response = input()
                if response == 'yes':
                    test = False
    #The query is added to the file at the top so it needs to be removed here
    #objects = ['ear', 'mouth', 'nose', 'hair']#
            objects[1:]
##    objects.sort(reverse=True)
        if using_oracle == True:
            if len(objects) > number - 1:
                objects = objects[0:number]
            print(objects)

        if using_oracle == True:
##        objects=[x[1] for x in objects]
##    v.calcanglesdists(v.db, v.ktosyns, query, objects)
            for objectsFromModule in objects:
                subprocess.call([sys.executable, "sim2_NotSavingExemplarInput.py", \
                                 bracketedquery + ",above," + objectsFromModule[1]])
        else:
            for objectsFromModule in objects:
                subprocess.call([sys.executable, "sim2_NotSavingExemplarInput.py", \
                                 bracketedquery + ",above," + objectsFromModule])

##    display.display_from_file("FromVisuoToDisplay"+query+".txt", number,
##                              add_background, image_output, cut_background)
        display.display_from_file("FromVisuoToDisplay"+query+".txt")
    else:
        display.display_from_file(image_name, from_imagenet=False, from_pkbm=True)

if __name__ == "__main__":
    main()
