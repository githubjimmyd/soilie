'''
Created on 2013-10-23

@author: Sebastien Ouellet sebouel@gmail.com
'''
import urllib
from urllib.request import urlopen
import tarfile
import sys
import re
import random
from nltk.corpus import wordnet
import requests

pattern = re.compile("_[0-9]+")

#annotation_url = "http://www.image-net.org/api/download/imagenet.bbox.synset?wnid="
bbox_url = "http://www.image-net.org/downloads/bbox/bbox/"
image_url = "http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid="

wordlist = open("wordlist.txt","r")
wordlist = [[word.strip() for word in line.split(",")] for line in wordlist]

#allwords = open("allwords.txt","r")
#allwords = [[word.strip() for word in line.split(",")] for line in allwords]

def retrieve(url, fname):
    with open(fname, "wb") as f:
        r = requests.get(url)
        f.write(r.content)

def download_image_nobb(synsets,query):
    for synset in synsets:
        id = str(synset.offset)
        if len(id) < 9:
            wnid = "n0"+id
        else:
            wnid = "n"+id
    
        images = urlopen(image_url+wnid)
        images_list = [image.split() for image in images]
        random.shuffle(images_list)
    
        
        for image in images_list:
            try:
                url = urlopen(image[1]).geturl()
                if url == image[1]:
                    print("Found one without bounding boxes")
##                    urllib.urlretrieve(url,"usable"+query+".jpg")
                    retrieve(url, "usable"+query+".jpg")
                    return "Image found"
            except:
                continue
        
    return "No image"



def download_image(wnid, query):
    """ Finds and downloads an available image from the web """
    images = urllib2.urlopen(image_url+wnid)
    images_list = [image.split() for image in images]
    random.shuffle(images_list)
    
##    urllib.urlretrieve(bbox_url+wnid+".tar.gz",wnid+".tar.gz")
    print(bbox_url+wnid)
##    urllib.urlretrieve(bbox_url+wnid,wnid+".tar.gz")
    retrieve(bbox_url+wnid+".tar.gz", wnid+".tar.gz")
    bb_files = tarfile.open(wnid+".tar.gz", "r:gz")
    names = bb_files.getnames()
    
    names = "".join(names)
    ids = re.findall(pattern, names)
    used_id = None
    
    for image in images_list:
        if re.findall(pattern,image[0])[0] in ids:
            try:
                url = urllib2.urlopen(image[1]).geturl()
                if url == image[1]:
                    used_id = image[0]+".xml"
##                    urllib.urlretrieve(url,"usable"+query+".jpg")
                    retrieve(url, "usable"+query+".jpg")
                    break
            except:
                continue
            
    for member in bb_files:
        if used_id in member.name:
            bbox = bb_files.extractfile(member)
            bbox_file = open("usable"+query+".xml","w")
            bbox_file.write(bbox.read())
            bbox_file.close()
            break
    
    bb_files.close()

def get_wnid(query):
    """ Finds the wnid associated with the query word"""
    wnid = None
    
    for line in wordlist:
        if query in line:
            wnid = line

    if wnid == None:
        print("No bounding boxes available for "+query)
        # We can avoid that for now
        synsets = wordnet.synsets(query,"n")
        return synsets, "Nobb"
    else:
        return wnid[0][-11:-2], "Yesbb"
    
def main(query=None):
    if query == None:
        query = sys.argv[1]
    
    wnid,flag = get_wnid(query)
    
    if wnid != None:
        if flag != "Nobb":
            download_image(wnid, query)
            return "Found"
        else:
            image_flag = download_image_nobb(wnid, query)
            if image_flag == "No image":
                return "Not found"
            else:
                return "Found nobb"
    else:
        return "Not found"
    
if __name__ == "__main__":
    main()
