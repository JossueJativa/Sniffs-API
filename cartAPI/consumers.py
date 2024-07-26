from channels.consumer import SyncConsumer

class CartConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("connected", event)

        self.send({
            "type": "websocket.accept"
        })

    def websocket_receive(self, event):
        print("receive", event)

        self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    def websocket_disconnect(self, event):
        print("disconnected", event)

        self.send({
            "type": "websocket.close"
        })