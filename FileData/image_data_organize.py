import os

directory_in_str = "/home/justin/darthmallocsarchive-svn/trunk/pkgForJustin/FileData/peekaboom/results/"
directory = os.fsencode(directory_in_str)
file_codes = []
image_name_dict = {}

stage = 0
for file in os.listdir(directory):
    filename = directory_in_str + os.fsdecode(file)
    with open(filename) as f:
        lines = [line.strip() for line in f]
        for i in range(len(lines)):
            print(lines[i])
            print("\n\n\n\n\n\n\n\n")
            if i == 0:
                dex = 5
                image_code = ""
                stop = False
                while stop == False:
                    if lines[i][dex] == ')':
                        stop = True
                        #print("stop")
                    else:
                        image_code = image_code + lines[i][dex]
                        dex += 1
                file_codes.append(image_code)
                image_name_dict[image_code] = []
            else:
                start = dex + 2
                spot = start
                stop = False
                name = ""
                while stop == False:
                    if lines[i][spot] == ')':
                        stop = True
                        #print("stop")
                    else:
                        name = name + lines[i][spot]
                        spot += 1
                #print(name)
                image_name_dict[image_code].append(name)
    #print("stage " + str(stage))
    stage += 1

image_name_data = open("image_names.txt", 'w')
for i in range(len(file_codes)):
    line = file_codes[i] + ':'
    for j in range(len(image_name_dict[file_codes[i]])):
        line = line + image_name_dict[file_codes[i]][j]
        if j < len(image_name_dict[file_codes[i]]) - 1:
            line = line + ','
    image_name_data.write(line+'\n')
    print(line)
    print("##########################")

image_name_data.close()
    
                
                        
                        
                        
        
    
