import json

class Snake:
    def __init__(self, id):
        self.pos = [(0,0)]
        self.colours = ['black']
        self.id = id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
            # sort_keys=True, indent=4)