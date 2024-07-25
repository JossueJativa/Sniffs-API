import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if user and user.is_authenticated:
            self.room_group_name = f'cart_{user.id}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action', '')
        user_id = text_data_json.get('user', '')
        product_id = text_data_json.get('product', '')
        quantity = text_data_json.get('quantity', 1)
        refresh = text_data_json.get('refresh', '')

        if action == 'add':
            response = {'status': 'success', 'message': 'Product added'}
        elif action == 'getQuantity':
            response = {'status': 'success', 'quantity': 0}
        elif action == 'getCart':
            response = {'status': 'success', 'cart': []}
        elif action == 'delete':
            response = {'status': 'success', 'message': 'Item deleted'}
        else:
            response = {'status': 'error', 'message': 'Invalid action'}

        await self.send(text_data=json.dumps(response))
