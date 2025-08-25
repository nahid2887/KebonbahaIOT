import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import IoTDevice, DeviceData
from asgiref.sync import sync_to_async


class OneWayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        # Get device_id from query params or message
        query_string = self.scope['query_string'].decode()
        device_id = None
        for part in query_string.split('&'):
            if part.startswith('device_id='):
                device_id = part.split('=', 1)[1]
        if not device_id:
            device_id = data.get('device_id')
        try:
            device_id = int(device_id)
        except (TypeError, ValueError):
            await self.send(text_data=json.dumps({'error': 'Invalid or missing device_id'}))
            return
        weight = data.get('weight')
        temperature = data.get('temperature')
        try:
            device = await sync_to_async(IoTDevice.objects.get)(id=device_id)
        except IoTDevice.DoesNotExist:
            await self.send(text_data=json.dumps({'error': 'Device not found'}))
            return
        await sync_to_async(DeviceData.objects.create)(device=device, weight=weight, temperature=temperature)
        # No response needed (one-way)


class TwoWayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        action = data.get('action')
        # Try to get device_id from query params first
        query_string = self.scope['query_string'].decode()
        device_id = None
        for part in query_string.split('&'):
            if part.startswith('device_id='):
                device_id = part.split('=', 1)[1]
        if not device_id:
            device_id = data.get('device_id')
        try:
            device_id = int(device_id)
        except (TypeError, ValueError):
            await self.send(text_data=json.dumps({'error': 'Invalid or missing device_id'}))
            return
        try:
            device = await sync_to_async(IoTDevice.objects.get)(id=device_id)
        except IoTDevice.DoesNotExist:
            await self.send(text_data=json.dumps({'error': 'Device not found'}))
            return
        if action == 'get_data':
            last_data = await sync_to_async(DeviceData.objects.filter(device=device).order_by('-timestamp').first)()
            if last_data:
                await self.send(text_data=json.dumps({
                    'weight': last_data.weight,
                    'temperature': last_data.temperature,
                    'timestamp': str(last_data.timestamp)
                }))
            else:
                await self.send(text_data=json.dumps({'error': 'No data'}))
        elif action == 'send_data':
            weight = data.get('weight')
            temperature = data.get('temperature')
            await sync_to_async(DeviceData.objects.create)(device=device, weight=weight, temperature=temperature)
            await self.send(text_data=json.dumps({'status': 'data saved'}))
