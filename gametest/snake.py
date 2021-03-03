import json

class Snake:
    def __init__(self, id):
        self.pos = [(0,0)]
        self.colours = ['black']
        self.id = id
        self.dir = 0
        self.tempdir = 0
        self.foodeaten = 0   
        self.len = 5
        self.digesting = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
            # sort_keys=True, indent=4)

class Food:
    def __init__(self, X, Y, colour='red', points=1):
        self.pos = (X, Y)
        self.colour = colour
        self. points = points
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
