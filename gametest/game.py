from gametest.snake import Snake
import random

class Game:
    height = 400
    width = 640
    max_food = 3

    room_attributes = {}
    online = set()

    def get_room(self, room_no, snake_id):
        if room_no not in self.room_attributes:
            return self.open_room(room_no, snake_id)
        self.room_attributes[room_no]['snakes'].append(Snake(snake_id))
        return self.room_attributes[room_no]

    def open_room(self, room_no, snake_id):

        self.room_attributes[room_no] = { 
            'food': self.gen_food(3, exclude_points = {(0,0)}), 
            'snakes': [Snake(snake_id)]
            }
        return self.room_attributes[room_no]
    
    def get_room_attributes(self, room_no):
        return self.room_attributes[room_no]


    def gen_food(self, amount, exclude_points = None):
        conj = []
        while len(conj) < amount:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            t = (x,y)
            if t not in exclude_points and t not in conj:
                conj.append(t)

        return conj

    def get_snake_id(self):
        id = 1 if len(self.online) == 0 else max(self.online)+1
        self.online.add(id)
        return id

    def update(self, snake_data, snake_id, room_no):
        snake = [ a for a in self.room_attributes[room_no]['snakes'] if a.id == snake_id ][0]
        # snake.pos = snake_data['pos']
        print("SNAKE DATA: " , snake_data)

    def leave(self, snake_id, room_no):
        if (len(self.room_attributes[room_no]['snakes']) == 1):
            del self.room_attributes[room_no]
            print('entrou aqui..')
        else:
            self.room_attributes[room_no]['snakes'] = [ a for a in self.room_attributes[room_no]['snakes'] if a.id != snake_id ]
        self.online.remove(snake_id)
