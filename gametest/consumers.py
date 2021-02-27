import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'roomname'
        self.room_group_name = 'chat_' + self.room_name

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
