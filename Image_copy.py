from shutil import copy
import json, os
"""
Architecture (list type)
image       [identifier], [imsize]
regions     [ansize], [boxcorners] or [vertices], [class], [type]
   - linegroup   [tags], [vertices]
version 
json = list type
regions = list type
linegroup = list type... but may be length = 1
box = dict[0]['regions'][0]['boxcorners']
polygon = dict[0]['regions'][0]['vertices']
line = dict[0]['regions'][0]['linegroup'][0]['vertices']
"""


CONCEPT_LIST = [ "Bus", "Car", "EmergencyVehicle", "Motorcycle", "RV", "TrafficSign", "Truck" ] # concept list

def load(filepath):
    fd = open(filepath)
    raf = json.loads(fd.read())
    fd.close()

    annotations = {}

    for image in raf:
        identifier = image['image']['identifier']
        if identifier in annotations.keys():
            print('identifier : ' + identifier + ' is already exist.')

        annotations[identifier] = image

    return annotations

def folder_make(folder_name, folder_path) :
    if not os.path.isdir(folder_path+folder_name) :
        os.mkdir(folder_path+folder_name)

def Image_copy() :
    for concept in CONCEPT_LIST :
        folder_path = "C:/Users/user/Desktop/화정/vehicle-1.0/"
        raf_file = "annotations_" + concept + ".raf"
        annotations_path = folder_path + raf_file
        annotations = load(annotations_path)
        folder_make(folder_name=concept, folder_path=folder_path) # make concept folder
        folder_path = folder_path + concept + "/"

        count = 0
        for image in annotations.keys() : # key is "image path & name"
            print("{} / {} / {}".format(concept, count, len(annotations.keys()) ))
            count+=1
            path_list = image.split("/")
            image_name = image.split("/")[-1]

            network_path = "//hm-win/Data/Avante/vehicle1.0/"
            copy_path = folder_path
            # make image path folder
            for path in path_list[:-1] :
                folder_make(folder_name=path, folder_path=copy_path)
                copy_path = copy_path + path + "/"
                network_path = network_path + path + "/"

            network_path = network_path + image_name
            target_path = copy_path + image_name
            copy(network_path, target_path)

def check_image():
    totalKey = []

    for concept in CONCEPT_LIST:
        folderPath = "C:/Users/user/Desktop/화정/vehicle-1.0/"
        rafPath = "annotations_" + concept + ".raf"
        annotations = load(folderPath + rafPath)

        totalKey += annotations.keys()
        continue

    print(len(totalKey))
    totalKey = list(set(totalKey))
    print(len(totalKey))

def copy_image():
    for a, b, c in os.walk("C:/Users/user/Desktop/화정/vehicle-1.0/Car"):
        print("{} contains the directories {} and the files {}".format(a, b, c))

copy_image()