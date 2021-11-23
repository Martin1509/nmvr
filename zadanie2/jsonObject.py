class Json():
    def __init__(self, x, y,sizeOfTile, actor, map, speed, rotation):
        self.x = x
        self.y = y
        self.speed = speed
        self.rotation = rotation
        self.sizeOfTile = sizeOfTile
        self.actor = actor
        self.map = map

class Actor():
    def __init__(self, x, y):
        self.x = x
        self.y = y