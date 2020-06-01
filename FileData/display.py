'''
Created on 2010-12-09

Display objects from a LabelMe database.

If you don't have a dataset, run the main method from labelmeretriever.

To do the first time you use a dataset from LabelMe:
Run the main method from xmlindexer. The data folder should be in the same folder as the xmlindexer and display script.
It will create an index file inside the data folder, which will then be used to search for objects.

One way to use the script:
1. Open a command prompt inside the folder in which the script is placed.
2. Launch the Python interpreter within the command prompt and import the module display
3. Write "imagine('the_object_to_be_displayed', (x,y))" where x and y are values between 0 and 1.
4. A window will appear displaying the object. Close it with either the Escape key or the Close button to summon another object.
5. The objects are kept in memory. If you want to reset the screen, write "clear()"

To display from a file:
3. Write "display_from_file('filename')"
    where "filename" is the actual filename, with extension, of the text file.

To use the Oracle of Objects:
3. Write "proximity('the_object_to_be_displayed')"

GrabCut from OpenCV can be enabled through the parameters, to process the LabelMe outlines.

Science of Imagination Laboratory

Author: Sebastien Ouellet - sebouel@gmail.com
'''

import os
import sys
import shutil
import math
import xml.dom.minidom
import random
import subprocess
from operator import itemgetter
from itertools import combinations

import pygame
import xmlindexer
import OracleScript
import numpy
#import segmentation

###################

# Only if OpenCV is installed. Decrease the number of iterations if too slow
doingGrabcut = False
doingGrabcutBG = False
grabcut_iterations = 5

white = (255,255,255)
pink = (255, 0, 255)
black = (0,0,0)
red = (255, 0, 0)

width = 1920
height = 1080

large_threshold = 500

to_display = [] #pygame.sprite.OrderedUpdates()
to_mask_display = [] #pygame.sprite.OrderedUpdates()
mask_details = []
current_picture = [None]
data_directory = xmlindexer.find_data()

oracle_threshold = 0.10

###################

if doingGrabcut or doingGrabcutBG:
    import cv2

class Full_Picture(pygame.sprite.Sprite):
    """ Full picture taken from the LabelMe dataset """
    def __init__(self, image, filename, thing):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.filename = filename
        self.called_from = thing


class Imagined(pygame.sprite.Sprite):
    """ Objects taken from the LabelMe images """
    def __init__(self,colors,pixels,box,position,color=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((box[2]-box[0],box[3]-box[1]),
                                    pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.colors = [x.copy() for x in colors]
        if color !=False and len(color) > 1:
            for c in self.colors:
                c[0], c[1], c[2] = color
        self.box = box
        self.offset_pixels(pixels)
        self.image_coloring()
        self.resize()
        self.rect.center = self.find_position(position)
        print self.rect.center
        self.put_inside_frame()

    def find_position(self,position):
        """ Assign a position to the object according to given values between 0 and 1, proportionally to the resolution """
        return (int(width*position[0]),int(height*position[1]))

    def offset_pixels(self,pixels):
        """ Offsets the position of the pixels so that they are adapted to the size of the object """
        self.pixels = []
        for pixel in pixels:
            self.pixels.append((pixel[0]-self.box[0],pixel[1]-self.box[1]))

    def image_coloring(self):
        """ Colors a blank surface with the pixels found in the database image """
        imagepixels = pygame.surfarray.pixels3d(self.image)
        imagealpha = pygame.surfarray.pixels_alpha(self.image)

        colors_and_pixels = zip(self.colors,self.pixels)
        for c_and_p in colors_and_pixels:
            imagepixels[c_and_p[1][0]][c_and_p[1][1]] = c_and_p[0]
            imagealpha[c_and_p[1][0]][c_and_p[1][1]] = 255

    def resize(self):
        image_width = self.rect.right - self.rect.left
        image_height = self.rect.bottom - self.rect.top

        if image_width > large_threshold or image_height > large_threshold:
            self.image = pygame.transform.scale(self.image, (image_width/2, image_height/2))

        self.rect = self.image.get_rect()

    def put_inside_frame(self):
        """ Repositions the image inside the frame """
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.bottom > height:
            self.rect.bottom = height

def cut_out(thing):
    """ Withdraw an unwanted known object from a full picture  """
    vertices = get_vertices(current_picture[0].filename, thing)
    pixels,box = inside_polygon(vertices)
    for pixel in pixels:
        pixel = ((pixel[0]-box[0],pixel[1]-box[1]))
    image_pixels = pygame.surfarray.pixels3d(current_picture[0].image)
    color = white
    for pixel in pixels:
        image_pixels[pixel[0]][pixel[1]] = color
    #Incomplete/Not used yet

def clear():
    """ Clears the objects to be displayed """
    global to_display
    to_display.empty()

def xml_to_jpg(filename):
    return filename[:-4]+".jpg"

def list_objects():
    """ Prints all objects in the current database """
    index = xml.dom.minidom.parse(os.path.join(data_directory,"index.xml"))
    for node in index.getElementsByTagName("object"):
        for node2 in node.getElementsByTagName("name"):
            for node3 in node2.childNodes:
                print node3.data

def retrieve(thing, all_files=False):
    """ Retrieves from the index file the filenames for the image and the annotations """
    index = xml.dom.minidom.parse(os.path.join(data_directory,"index.xml"))
    files = []
    for node in index.getElementsByTagName("object"):
        for node2 in node.getElementsByTagName("name"):
            for node3 in node2.childNodes:
                if node3.data == thing:
                    for node4 in node.getElementsByTagName("file"):
                            for node5 in node4.childNodes:
                                files.append(node5.data)

    if len(files) == 0:
        print "No object of that name:'"+thing+"' was found"
        return []
    else:
        if all_files:
            return files
        else:
            annotation = random.choice(files)
            image = xml_to_jpg(annotation)
            return [annotation,image]

def retrieve_multi(things, num=False):
    """Retrieves from the index file the filenames that have 'num' of the images present."""
    index = xml.dom.minidom.parse(os.path.join(data_directory,"index.xml"))
    files = [[thing, []] for thing in things]
    for i, thing in enumerate(things):
        for node in index.getElementsByTagName("object"):
            for node2 in node.getElementsByTagName("name"):
                for node3 in node2.childNodes:
                    if node3.data == thing:
                        for node4 in node.getElementsByTagName("file"):
                                for node5 in node4.childNodes:
                                    files[i][1].append(node5.data)
    if sum([len(files_[1]) for files_ in files]) == 0:
        temp = ["Background for '"]
        temp.extend(things)
        temp.append("' was not possible")
        print ''.join(temp)
        return []
    if num:
        options = sorted(range(2,num+1), reverse=True)
    else:
        options = sorted(range(2, len(things)+1), reverse=True)
    for option in options:
        combos = combinations([files_ for files_ in files if len(files_[1]) > 0], option)
        for combo in combos:
            possible = set(combo[0][1])
            for images in combo[1:]:
                possible &= set(images[1])
            if len(possible) > 0:
                return [random.choice(list(possible)), [x[0] for x in combo]]
    for files_ in files:
        if len(files_[1]) > 0:
            return [random.choice(files_[1]), [files[0]]]
    

def get_things_from_file(annotation,thing):
    objects = []
    document = xml.dom.minidom.parse(os.path.join(data_directory,annotation))

    for element in document.getElementsByTagName("object"):
        for name in element.getElementsByTagName("name"):
            for name_text in name.childNodes:
                if name_text.data.strip() == thing:
                    objects.append(element)
##    print annotation, thing, objects
##    print
    return objects

def get_vertices(annotation,thing):
    """ Parses the annotation file and returns all vertices for a given object, choosing randomly among the many similar objects in that scene """
    vertices_x = []
    vertices_y = []

    things = get_things_from_file(annotation,thing)
    if things == []:
        return False

    element = random.choice(things)

    for polygon in element.getElementsByTagName("polygon"):
        for point in polygon.getElementsByTagName("pt"):
            for x in point.getElementsByTagName("x"):
                for x_text in x.childNodes:
                    vertices_x.append(int(x_text.data))
            for y in point.getElementsByTagName("y"):
                for y_text in y.childNodes:
                    vertices_y.append(int(y_text.data))

    vertices = zip(vertices_x,vertices_y)

    return vertices

def get_image(image_name):
    """ Loads the image from the database in the most simple way possible """
    image = pygame.image.load(os.path.join(data_directory,image_name))
    return image

def bounding_box(vertices):
    """ Returns a box bounding the coordinates of pixels for a given polygon """
    sorted_vertices = sorted(vertices)

    x_min = sorted_vertices[0][0]
    x_max = sorted_vertices[-1][0]

    sorted_vertices = sorted(vertices,key=itemgetter(1))

    y_min = sorted_vertices[0][1]
    y_max = sorted_vertices[-1][1]

    return [x_min, y_min, x_max-1, y_max-1]

def grabcut_object(vertices, image_name):
    """ Uses the GrabCut function from OpenCV 2.31 to get a better outline for an object """
    box = bounding_box(vertices)
    cv_image = cv2.imread(os.path.join(data_directory,image_name))
    height, width = cv_image.shape[:2]
    mask = numpy.zeros((height, width), dtype='uint8')

    rect_width = box[2]-box[0]
    rect_height = box[3]-box[1]
    rect = (box[0],box[1],rect_width,rect_height)

    bgd = numpy.zeros((1, 13*5))
    fgd = numpy.zeros((1, 13*5))

    cv2.grabCut(cv_image, mask, rect, bgd, fgd, grabcut_iterations, mode=cv2.GC_INIT_WITH_RECT)

    pixels = []
    for y in xrange(box[1],box[3]):
        for x in xrange(box[0],box[2]):
            if mask[y][x] == 3:
                pixels.append((x,y))
    return pixels, box


def inside_polygon(vertices):
    """ Returns a list of pixels found within a given polygon """
    # !!! There is a memory leak in the current version of Pygame, whenever a surface is created.
    box = bounding_box(vertices)

    screen = pygame.Surface((box[2],box[3]))
    screen.fill(white)
    pygame.draw.polygon(screen, black, vertices)
    pixelscreen = pygame.surfarray.pixels2d(screen)
    pixelarray = numpy.array(pixelscreen)

    pixels = []
    x = box[0]
    while x < box[2]:
        y = box[1]
        while y < box[3]:
            if pixelarray[x][y] == 0:
                pixels.append((x,y))
            y += 1
        x += 1

    return pixels,box

def cut_out_background(background, img_and_objs):
    masks = []
    annotation = img_and_objs[0]
    image_name = xml_to_jpg(annotation)
    image = get_image(image_name)
    for object_ in img_and_objs[1]:
        mask = pygame.Surface((width,height), pygame.SRCALPHA, 32)
        mask.fill(black)
        vertices = get_vertices(annotation, object_)
        if vertices == False:
            continue
        pixels, box = grabcut_object(vertices, image_name)
##        pygame.draw.polygon(mask, white, vertices)
        colors = fill_surface(image, pixels)
        imagepixels = pygame.surfarray.pixels3d(mask)
        imagealpha = pygame.surfarray.pixels_alpha(mask)

        colors_and_pixels = zip(colors, pixels)
        for c_and_p in colors_and_pixels:
            imagepixels[c_and_p[1][0]][c_and_p[1][1]] = c_and_p[0]
            imagealpha[c_and_p[1][0]][c_and_p[1][1]] = 255
        masks.append(mask)
    return masks

def cut_surface(surface,pixels):
    """ Returns the colors of the given coordinates from the given surface """
    pixelsurface = pygame.surfarray.pixels3d(surface)
    pixelarray = numpy.array(pixelsurface)

    colors = []
    for pixel in pixels:
        #print pixel
        if len(pixel) > 1:
            #print len(pixelarray), len(pixelarray[0])
            if len(pixelarray) > pixel[0]:
                if len(pixelarray[pixel[0]]) > pixel[1]:
                    colors.append(pixelarray[pixel[0]][pixel[1]])

    #colors = [pixelarray[pixel[0]][pixel[1]] for pixel in pixels]

    return colors

def fill_surface(surface,pixels):
    """ Returns white for each pixel"""
    pixelsurface = pygame.surfarray.pixels3d(surface)
    pixelarray = numpy.array(pixelsurface)

    colors = []
    for pixel in pixels:
        #print pixel
        if len(pixel) > 1:
            #print len(pixelarray), len(pixelarray[0])
            if len(pixelarray) > pixel[0]:
                if len(pixelarray[pixel[0]]) > pixel[1]:
                    colors.append(white)

    #colors = [pixelarray[pixel[0]][pixel[1]] for pixel in pixels]

    return colors

def find_objects(picture):
    """ Returns the objects present in the picture """
    objects = []
    document = xml.dom.minidom.parse(os.path.join(data_directory,picture))
    for node_object in document.getElementsByTagName("object"):
        for node_name in node_object.getElementsByTagName("name"):
            for node_actualname in node_name.childNodes:
                objects.append(node_actualname.data)
    return objects

def fewest_picture_selection(pictures):
    """ Chooses a picture as uncluttered as possible """
    selected = ""
    minimum = 99999
    for picture in pictures:
        number = len(find_objects(picture))
        if number < minimum:
            minimum = number
            selected = picture

    return selected

def segmentation_picture_selection(pictures):
    """ Ignores LabelMe annotation and looks at the image itself for clutter """
    selected = ""
    polygons_list = [segmentation.segment(picture) for picture in pictures]
    #Incomplete

def window(things):
    """ Generates a window where the desired objects would be, used to choose a convenient picture """
    windows = []
    #Incomplete

def test_margins(position):
    """ Keeps the displayed object in the visible screen area """
    if position > 1.0:
        position = 1.0
        print "Warning: out of picture, needs to adjust the position. The original values can't be applied"
    elif position < 0.0:
        position = 0.0
        print "Warning: out of picture, needs to adjust the position. The original values can't be applied"
    return position

def find_position(angle, distance, main_position):
    """ Calculates a position given a relative distance and an angle (from 0 to 180, positive or negative) from a given position """
    y_direction = -1
    if angle < 0:
        y_direction = 1
        angle = math.fabs(angle)
    radian_angle = math.radians(angle)
    x_factor = math.cos(radian_angle)
    y_factor = math.sin(radian_angle)
    x_distance = x_factor*(distance/2.0)
    y_distance = y_direction*y_factor*(distance/2.0)
    x_position = main_position[0]+x_distance
    y_position = main_position[1]+y_distance
    x_position = test_margins(x_position)
    y_position = test_margins(y_position)

    return [x_position,y_position]

def full_picture(thing, draw=True):
    """ Looks for a picture containing the object wanted """
    pictures = retrieve(thing,all=True)
    if len(pictures) == 0:
        pass
    else:
        selected = fewest_picture_selection(pictures)
        selected_image = get_image(xml_to_jpg(selected))
        picture = Full_Picture(selected_image, selected, thing)
        to_display.add(picture)
        current_picture[0] = picture
        if draw:
            draw_everything()

def proximity(thing):
    """ Calls the imagine method after calling the Oracle of Object and display all objects above a threshold """
    objects = [thing]
    oracle_answers = OracleScript.proximity(thing)
    for item in oracle_answers:
        if float(oracle_answers[item]) > oracle_threshold:
            objects.append(item)
    if len(objects) > 4:
        objects = objects[0:5]
    for item in objects:
        print item
        imagine(item, (random.random(),random.random()), draw=False)
    draw_everything()

def imagine(thing, position=(0.5,0.5), draw=True, grabcut=doingGrabcut, color=False):
    """ Finds an appropriate image and transforms it. Display it at a given position in the format (x,y), where x and y are between 0 and 1 """
    things = retrieve(thing)
    if len(things) == 0:
        pass
    else:
        image_name = things[1]
        annotation = things[0]
        vertices = get_vertices(annotation,thing)
        image = get_image(image_name)
        if grabcut:
            pixels, box = grabcut_object(vertices, image_name)
        else:
            pixels,box = inside_polygon(vertices)

        colors = cut_surface(image,pixels)

        if color:
            #imagined = Imagined(colors,pixels,box,position,color)
            mask = pygame.Surface(image.get_size(), pygame.SRCALPHA, 32)
            mask.fill(black)
            mask_colors = [x.copy() for x in colors]
            for c in mask_colors:
                c[0], c[1], c[2] = color
            imagepixels = pygame.surfarray.pixels3d(mask)
            imagealpha = pygame.surfarray.pixels_alpha(mask)
            colors_and_pixels = zip(mask_colors, pixels)
            for c_and_p in colors_and_pixels:
                imagepixels[c_and_p[1][0]][c_and_p[1][1]] = c_and_p[0]
                imagealpha[c_and_p[1][0]][c_and_p[1][1]] = 255
            to_mask_display.append(mask)
            mask_details.append([thing, image_name, color])
            
        
        imagined2 = Imagined(colors,pixels,box,position)
        to_display.append(imagined2)

##        print thing

        if draw:
            draw_everything()

def make_mask_colors(num, num2=1001):
    #No longer used
    """Returns a list of color triples for the mask."""
    #2304 color/object max
    mask_colors = []
    x = int(math.floor(256*9/float(num2)))
    setup = {0 : [0, 0, 0, 0], 256 : [1, 255, 0, 0], 512 : [2, 255, 255, 0],
             768 : [1, 0, 0, 0], 1024 : [0, 0, 255, 0], 1280 : [2, 255, 255, 0],
             1536 : [2, 0, 0, 0], 1792 : [0, 0, 0, 255],
             2048 : [1, 255, 0, 255]}
    for inc in range(x, 256*9, x):
        color = []
        for val in sorted(range(0, 2049, 256), reverse=True):
            if inc > val:
                color = setup[val]
                break
        i = color[0]
        color = color[1:]
        color[i] += inc%256
        mask_colors.append(color)
    return random.sample(mask_colors, num)

def display_from_file(filename, num, add_background=False,
                      image_output=False, cut=False):
    """ Parses a text file to display objects """
    main_directory = os.path.dirname(sys.argv[0])
    f = open(os.path.join(main_directory,filename), "r")
    main_object = "None"
    main_position = [0.5,0.5]
    objects = []
    angledist = []
##    if image_output:
    colors = [white for x in range(num)]
##    else:
##        colors = [False for x in range(num)]
##    print colors
    for line in f:
        if line[0]== "#":
            main_object = line[1::].rstrip("\n")
            objects.append(main_object)
##            imagine(main_object, main_position, draw=False, color=colors[i])
        else:
            first_index = 0
            for character in line:
                first_index += 1
                if character == "-":
                    break
            second_index = 0
            for character in line:
                if character == " ":
                    break
                second_index += 1
            item = line[first_index:second_index]
            objects.append(item)
            first_index = second_index+1
            second_index = first_index
            for character in line[second_index::]:
                if character == " ":
                    break
                second_index += 1
            angle = eval(line[first_index:second_index])
            distance = eval(line[second_index+1::])
            angledist.append([angle, distance])
    
##            position = find_position(angle, distance, main_position)
##            imagine(item, position, draw=doingGrabcut, color=colors[i])
    if add_background:
        img_and_objs = retrieve_multi(objects, num=False)
        if img_and_objs == []:
            print 'fail'
            background = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            background.fill(white)
        else:
            background = pygame.image.load(os.path.join(data_directory,
                                                        xml_to_jpg(img_and_objs[0])))
            #Too lazy to do all the refactoring necessary to make this call local
            globals()['width'], globals()['height'] = background.get_size()
            if cut:
                background_masks = cut_out_background(background, img_and_objs)
    else:
        background = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        background.fill(white)
    imagine(objects[0], main_position, draw=False, grabcut=doingGrabcut, color=colors[0])
    for i, object_ in enumerate(objects[1:]):
        angle, distance = angledist[i]
        position = find_position(angle, distance, main_position)
        imagine(object_, position, draw=False, grabcut=doingGrabcut, color=colors[i+1])
    if cut:
        make_everything(background, background_masks, image_output)
    else:
        draw_everything(background, image_output)

def make_everything(background, background_masks, image_output):

    i = 0
    while True:
        try:
            os.mkdir('temp'+str(i))
        except OSError:
            i += 1
        else:
            #os.mkdir(os.path.join('temp'+str(i), 'src'))
            break
    shutil.copyfile('InpaintImageMain.exe',
                    os.path.join('temp'+str(i), 'InpaintImageMain.exe'))
    shutil.copyfile('cloning.exe', os.path.join('temp'+str(i), 'cloning.exe'))
    os.chdir('temp'+str(i))
    pygame.image.save(background, 'background.jpg')
    for k, mask in enumerate(background_masks):
        pygame.image.save(mask, 'background_mask.jpg')
        pygame.image.save(mask, ''.join(['background_mask', str(k), '.jpg']))
        subprocess.call(["InpaintImageMain.exe"])
    temp = pygame.sprite.OrderedUpdates()
    
    for j, sprite in enumerate(to_display):
        temp.add(sprite)
        dst_mask = pygame.Surface((width,height), pygame.SRCALPHA, 32)
        dst_mask.fill(black)
        pos = sprite.rect.center
        pygame.draw.line(dst_mask, red, pos, (pos[0]+1, pos[1]), 2)
        pygame.image.save(dst_mask, 'dest_mask.png')
        pygame.image.save(dst_mask, ''.join([str(j), 'dest_mask', '.png']))
        src_mask = to_mask_display[j]
        pygame.image.save(src_mask, 'source_mask.png')
        pygame.image.save(src_mask, ''.join([str(j), 'source_mask', '.png']))
        src = mask_details[j]
        shutil.copyfile(os.path.join(data_directory,src[1]), 'source.jpg')
        shutil.copyfile(os.path.join(data_directory,src[1]), ''.join([str(j), 'source', '.jpg']))
        subprocess.call(['cloning.exe'])

    if image_output:        
        check = pygame.Surface((width,height), pygame.SRCALPHA, 32)
        check.fill(white)
        temp.draw(background)
        temp.draw(check)
        pygame.image.save(background, 'bgcheck.jpg')
        pygame.image.save(check, 'check.jpg')
    else:
        pygame.init()
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption('SOILIE\'S IMAGINED SCENE')
        temp.draw(background)
        screen.blit(background)
        pygame.display.flip()
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
            to_display.draw(screen)
            pygame.display.flip()

        pygame.quit()
##    f = open(os.path.join('temp'+str(i), 'associations.txt'), 'w')
##    f.write('name_of_file.jpg\n')
##    f.write('Label Source Color\n')
##    for pic in mask_details:
##        f.write(' '.join(pic[:2]+[str(pic[2])]))
##        f.write('\n')
##        shutil.copyfile(os.path.join(data_directory,pic[1]),
##                        os.path.join('temp'+str(i), 'src', pic[1]))
##    f.close()
    return


def draw_everything(background, image_output):
    """ Display all objects in the to_display group """

    temp = pygame.sprite.OrderedUpdates()
    for s in to_display:
        temp.add(s)

    if image_output:
        temp.draw(background)
        pygame.image.save(background, 'bgcheck.jpg')
    else:
        pygame.init()

        screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
        pygame.display.set_caption('SOILIE\'S IMAGINED SCENE')

        temp.draw(background)
        screen.blit(background, (0, 0))

        pygame.display.flip()

        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False

        pygame.quit()
