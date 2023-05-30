import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

#from .tasks import get_response
import sys
sys.path.append("c:/users/skikk/appdata/local/programs/python/python39/lib/site-packages")
import requests

class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data):
        category = requests.get("http://127.0.0.1:5000/reply?question="+text_data_json["text"])
        print(category)
        text_data_json = json.loads(text_data)
        #get_response.delay(self.channel_name, text_data_json)

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "chat_message",
                "text": {"msg": text_data_json["text"], "source": "user"},
            },
        )

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "chat.message",
                "text": {"msg": "Your question belongs to the: '" + category + "' category", "source": "bot"},
            },
        )

    def chat_message(self, event):
        text = event["text"]
        self.send(text_data=json.dumps({"text": text}))
