from gametest.game import Game
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class GameConsumer(WebsocketConsumer):
    game = Game()
    users = {}
    
    def connect(self):
        room = '222' # TODO: to be changed
        self.room_group_name = 'game_' + room

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )
        self.users[self.channel_name] ={'id' : self.game.get_snake_id() }
        # vai adicionar o pc q se ligou a esse grupo / sala
        self.accept()

    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.game.leave(self.users[self.channel_name]['id'], self.users[self.channel_name]['room'])
        del self.users[self.channel_name]

    def receive(self, text_data):
        data_json = json.loads(text_data)

        # send msg to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': data_json['type'], 
                # vai enviar isto para uma funcao c o mm nome dessa cena
                'message':data_json
            }
        )

    def join(self, event):
        message = event['message']
        print(event)
        # to send back:
        # - all food positions
        # - his snake id
        # snake_id = self.game.get_snake_id()

        snake_id = self.users[self.channel_name]['id']
        room_no = int(message['room_no'])
        self.users[self.channel_name]['room'] = room_no
        
        room = self.game.get_room(room_no)
        # if room is not None:
        #     self.poll_current()
        
        if room is None:
            room = self.game.create_room(room_no)
        self.game.add_snake_to_room(room_no, snake_id)

        # room_info = self.game.get_room(222, snake_id).copy()
        room_info = room.copy()
        room_info['snakes'] = [ a.toJSON() for a in room_info['snakes'] ]
        # send msg to websocket
        self.send(text_data=json.dumps({
            'type' : 'websocket.send',
            'data' : {
            'snake_id': snake_id,
            'room': room_info
            },
            'tp' : 'join'
        }))
        self.poll_current()


    def poll_current(self):
        self.send(text_data=json.dumps({
            'type' : 'websocket.send',
            'tp' : 'polling'
        }))

    def poll_answer(self, events):
        message = events['message']
        # self.game.update(message['snake'])
        room_no = self.users[self.channel_name]['room']
        # self.game.update(message['snake'], message['snake_id'], room_no)
        print('\n', message)
        self.send(text_data=json.dumps({
            'type' : 'websocket.send',
            'tp' : 'update',
            'data' : {
                'snake' : message['snake'], 
                'id' : message['snake_id'],
            }
        }))        

    def move(self, events):
        message = events['message'] # ['message']
        # { snake : [ pos : [], colours : []], snake_id, direcao }
        # print(message)
        room = self.users[self.channel_name]['room']
        self.game.update(message['snake'], message['snake_id'], room)
        self.send(text_data=json.dumps({
            'type' : 'websocket.send',
            'tp' : 'move',
            'data' : {
                'snake' : message['snake'], 
                'id' : message['snake_id'],
                'newdir' : message['newdir']
            }
        }))

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.channel_name 
        # is automatically attributed to the other person

        # self.room_name = 'roomname'
        self.room_group_name = 'chat_' + 'roomname' #self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def chat_message(self, event):
        message = event['message']

        # send msg to websocket
        self.send(text_data=json.dumps({
            'type' : 'websocket.send',
            'message':message
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json # ['message']
        print('receive : ', message)

        # send msg to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message', 
                # este type vai chamar uma funcao 
                # com esse nome q vai enviar a mensagem!
                # é tipo um callback
                'message':message
            }
        )

        # self.send(text_data=json.dumps({
        #     'message':message
        # }))
