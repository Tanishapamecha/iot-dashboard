from channels.generic.websocket import AsyncJsonWebsocketConsumer

class TelemetryConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("telemetry", self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("telemetry", self.channel_name)

    async def telemetry_event(self, event):
        data = event.get("data")
        await self.send_json(data)
