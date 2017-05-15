import json, os
from collections import defaultdict

path = "./annotations.raf"

def folder_make(folder) :
    if not os.path.isdir(folder) :
        os.mkdir(folder)

with open(path) as json_file:
    Architecture = json.load(json_file)
    image_dict = defaultdict(list)
    information = ""
    for i,_ in enumerate(Architecture) :
        folder_name = Architecture[i]['image']['identifier'].split("/")[0]
        image_dict[folder_name].append(Architecture[i])
        folder_make(folder_name)

    for key in image_dict :
        image_dict[key] = sorted(image_dict[key], key=lambda value : value['image']['identifier'])
        output_path = "./" + key + "/annotations.raf"
        with open(output_path, 'w') as outfile :
            json.dump(image_dict[key], outfile, indent=4)



