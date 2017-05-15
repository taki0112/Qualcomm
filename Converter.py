import json

IM_PATH = "./annotations_IM.raf"
Shape_PATH = "./annotations_Shape.raf"


def IM_to_Shape() :
    # added "id", "properties", "score"
    # properties dict type
    # properties = negative, occluded, shape, text

    IM_annotations = load(IM_PATH)

    for key in IM_annotations.keys() : # key is "image path & name"
        for i,_ in enumerate(IM_annotations[key]['regions']) :
            properties = dict()

            # add id, score
            IM_annotations[key]['regions'][i]['id'] = IM_annotations[key]['regions'][i]['tags'][0].split(":")[1]
            IM_annotations[key]['regions'][i]['score'] = IM_annotations[key]['regions'][i]['tags'][3].split(":")[1]

            # set properties
            properties['negative'] = IM_annotations[key]['regions'][i]['tags'][1].split(":")[1]
            properties['occluded'] = IM_annotations[key]['regions'][i]['tags'][2].split(":")[1]
            properties['shape'] = IM_annotations[key]['regions'][i]['tags'][4].split(":")[1]
            properties['text'] = IM_annotations[key]['regions'][i]['tags'][5].split(":")[1]

            # remove tags
            del IM_annotations[key]['regions'][i]['tags']

            # add properties
            IM_annotations[key]['regions'][i]['properties'] = properties

    save(IM_annotations, Shape_PATH)


def Shape_to_IM() :
    # added tags
    # tags list type... (id, properties, score)
    Shape_annotations = load(Shape_PATH)

    for key in Shape_annotations.keys() : # key is "image path & name"
        for i,_ in enumerate(Shape_annotations[key]['regions']) :
            tags = list()

            # set tags
            id = "id:{}".format(Shape_annotations[key]['regions'][i]['id'])
            score = "score:{}".format(Shape_annotations[key]['regions'][i]['score'])
            negative = "negative:{}".format(Shape_annotations[key]['regions'][i]['properties']['negative'])
            occluded = "occluded:{}".format(Shape_annotations[key]['regions'][i]['properties']['occluded'])
            shape = "shape:{}".format(Shape_annotations[key]['regions'][i]['properties']['shape'])
            text = "text:{}".format(Shape_annotations[key]['regions'][i]['properties']['text'])

            # remove key, value
            del Shape_annotations[key]['regions'][i]['id']
            del Shape_annotations[key]['regions'][i]['score']
            del Shape_annotations[key]['regions'][i]['properties']

            # add tags
            tags.extend([id, negative, occluded, score, shape, text])
            tags = sorted(tags, key = lambda str : str.split(":")[0])
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