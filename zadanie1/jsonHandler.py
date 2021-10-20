import json
import jsonObject


def getJsonObject(pathToJson):

    object = {}
    with open(pathToJson, "r") as read_file:
        dict = json.load(read_file) 
        object = jsonObject.Json(**dict)

    return object

def changeJson(pathToJson,object):
    with open(pathToJson, "w") as read_file:
        json.dump(object, read_file, ensure_ascii=False, indent=4)


def createJsonObject(x,y,sizeOfTile,actorX,actorY,map):
    object  = {
        "x": x,
        "y": y,
        "sizeOfTile": sizeOfTile,
        "actor": {
            "x": actorX,
            "y": actorY
        },
        "map": map
    }
    return object