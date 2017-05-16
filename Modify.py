import json
from collections import Counter
from pprint import pprint

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


def save(annotations, filepath):
    raf = []
    with open(filepath, 'w') as fd:
        for identifier in sorted(annotations.keys()):
            raf.append(annotations[identifier])

        fd.write(json.dumps(raf, sort_keys=True, indent=4))

def Modify() :
    Tool_path = "D:/annotation/holland1/back_up/annotations.raf"
    IM_path = "C:/Users/user/Desktop/화정/annotations_holland.raf"
    save_path = "C:/Users/user/Desktop/화정/annotations_Tool_modify.raf"

    Tool_annotaions = load(Tool_path)
    IM_annotations = load(IM_path)
    len_set = set()
    compare = lambda x,y : Counter(x) == Counter(y)
    for key in IM_annotations.keys() : # key is "image path & name"
        try :
            for i, _ in enumerate(IM_annotations[key]['regions']):
                if ( len(IM_annotations[key]['regions']) == len(Tool_annotaions[key]['regions']) ) and ( IM_annotations[key]['regions'][i]['vertices'] == Tool_annotaions[key]['regions'][i]['vertices']):
                    IM_annotations[key]['regions'][i]['id'] = Tool_annotaions[key]['regions'][i]['id']
                    IM_annotations[key]['regions'][i]['score'] = Tool_annotaions[key]['regions'][i]['score']
                    IM_annotations[key]['regions'][i]['properties'] = Tool_annotaions[key]['regions'][i]['properties']
                else :
                    len_set.add(key)
                    # print("len x!!!   "+key)

        except KeyError :
            print("key error   " + key)

    print(len(len_set))
    pprint(len_set)
    save(IM_annotations,save_path)

Modify()


