import json, os
from collections import defaultdict

# IM_PATH = "D:/annotation/Image_Miner/"
# Shape_PATH = "D:/annotation/"
# NAME = "/annotations.raf"

FILE_LIST = ["ave_6", "crosswalk", "easyNYC", "R8_sunny_0302", "SDDT_0418", "SDDT_R1", "time_square", "wall2",
             "wall2_2", "wall3"]


def Set_properties(**annotations):
    properties = dict()
    for property in annotations['tags']:
        property_name = property.split(":")[0]
        property_value = property.split(":")[1]

        if (property_name.__eq__('id')):
            annotations[property_name] = int(property_value)
        elif (property_name.__eq__('score')):
            annotations[property_name] = float(property_value)
        else:
            properties[property_name] = property_value

    # remove tags
    del annotations['tags']

    # add properties
    annotations['properties'] = properties

    return annotations


def IM_to_Shape(IM_PATH, Shape_PATH):
    # IM_PATH : A raf file that already exists
    # Shape_PATH : A raf file to be created

    # added "id", "properties", "score"
    # properties dict type
    # properties = negative, occluded, shape, text

    IM_annotations = load(IM_PATH)

    for key in IM_annotations.keys():  # key is "image path & name"
        for i, _ in enumerate(IM_annotations[key]['regions']):
            try:
                IM_annotations[key]['regions'][i] = Set_properties(**IM_annotations[key]['regions'][i])
            except KeyError:  # if the annotations key does not have 'tags', it's a new addition
                pass

    save(IM_annotations, Shape_PATH)


def Shape_to_IM(Shape_PATH, IM_PATH):
    # Shape_PATH : A raf file that already exists
    # IM_PATH : A raf file to be created

    # added tags
    # tags list type... (id, properties, score)
    Shape_annotations = load(Shape_PATH)
    for key in Shape_annotations.keys():  # key is "image path & name"
        for i, _ in enumerate(Shape_annotations[key]['regions']):
            tags = list()

            # set tags
            id = "id:{}".format(Shape_annotations[key]['regions'][i]['id'])
            score = "score:{}".format(Shape_annotations[key]['regions'][i]['score'])
            negative = "negative:{}".format(Shape_annotations[key]['regions'][i]['properties']['negative'])
            occluded = "occluded:{}".format(Shape_annotations[key]['regions'][i]['properties']['occluded'])
            shape = "shape:{}".format(Shape_annotations[key]['regions'][i]['properties']['shape'])
            text = "text:{}".format(Shape_annotations[key]['regions'][i]['properties']['text'])

            """
            improve performance "set tags" code (only negative, occluded, shape, text ... no id & score) 

            for tags_key in Shape_annotations[key]['regions'][i]['properties'].keys() :
                value = tags_key+":{}".format(Shape_annotations[key]['regions'][i]['properties'][tags_key])
                tags.extend(value)
            """

            # remove id, score, properties
            del Shape_annotations[key]['regions'][i]['id']
            del Shape_annotations[key]['regions'][i]['score']
            del Shape_annotations[key]['regions'][i]['properties']

            # add tags
            tags.extend([id, negative, occluded, score, shape, text])
            tags = sorted(tags, key=lambda str: str.split(":")[0])
            Shape_annotations[key]['regions'][i]['tags'] = tags

    save(Shape_annotations, IM_PATH)


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


def folder_make(folder_name, folder_path):
    if not os.path.isdir(folder_path + folder_name):
        os.mkdir(folder_path + folder_name)


def Merge(Shape_list, IM_list, Merge_path):
    RAF = "/annotations.raf"
    annotations = dict()
    for identifier in FILE_LIST:
        Shape_to_IM(Shape_list + identifier + RAF, IM_list + identifier + RAF)
        annotations.update(load(IM_list + identifier + RAF))

    save(annotations, Merge_path)  # save merged annotations.raf
    print("Merge finish")


def Categorization(raf_path, folder_path):
    with open(raf_path) as raf_file:
        Architecture = json.load(raf_file)
        image_dict = defaultdict(list)
        for i, _ in enumerate(Architecture):
            folder_name = Architecture[i]['image']['identifier'].split("/")[0]
            image_dict[folder_name].append(Architecture[i])
            folder_make(folder_name, folder_path)

        for identifier in image_dict:
            image_dict[identifier] = sorted(image_dict[identifier], key=lambda value: value['image']['identifier'])
            output_path = folder_path + identifier + "/annotations.raf"
            with open(output_path, 'w') as outfile:
                json.dump(image_dict[identifier], outfile, indent=4)


def main():
    select = 123

    if select == 123:  # IM_to_Shape
        folder_path = "C:/Users/user/Desktop/화정/"

        raf_file = folder_path + "annotations.raf"
        os.rename(raf_file, folder_path + "annotations_IM.raf")

        im_path = folder_path + "annotations_IM.raf"
        shape_path = folder_path + "annotations.raf"

        IM_to_Shape(im_path, shape_path)
        print("IM_to_Shape finish")

        Categorization(raf_path=shape_path, folder_path=folder_path)
        print("Categorization finish")

    elif select == 789:  # Shape_to_IM
        Shape_list = "D:/annotation/"
        IM_list = "D:/annotation/Image_Miner/"
        Merge_path = "D:/annotation/Image_Miner/_Merge/annotations.raf"

        Merge(Shape_list=Shape_list, IM_list=IM_list, Merge_path=Merge_path)


main()