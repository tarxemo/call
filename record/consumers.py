import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = f"user_{self.user.id}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "call":
            await self.initiate_call(data)
        elif action == "accept":
            await self.accept_call(data)
        elif action == "reject":
            await self.reject_call(data)
        elif action == "offer":
            await self.forward_signal(data, "offer")
        elif action == "answer":
            await self.forward_signal(data, "answer")
        elif action == "ice_candidate":
            await self.forward_signal(data, "ice_candidate")

    async def initiate_call(self, data):
        target_user_id = data["target_user"]
        await self.channel_layer.group_send(
            f"user_{target_user_id}",
            {
                "type": "call_request",
                "caller_id": self.user.id,
                "caller_name": self.user.username,
            }
        )

    async def call_request(self, event):
        await self.send(text_data=json.dumps({
            "action": "incoming_call",
            "caller_id": event["caller_id"],
            "caller_name": event["caller_name"],
        }))

    async def accept_call(self, data):
        caller_id = data["caller_id"]
        await self.channel_layer.group_send(
            f"user_{caller_id}",
            {
                "type": "call_accepted",
                "callee_id": self.user.id,
                "callee_name": self.user.username,
            }
        )

    async def call_accepted(self, event):
        await self.send(text_data=json.dumps({
            "action": "call_accepted",
            "callee_id": event["callee_id"],
            "callee_name": event["callee_name"],
        }))

    async def reject_call(self, data):
        caller_id = data["caller_id"]
        await self.channel_layer.group_send(
            f"user_{caller_id}",
            {
                "type": "call_rejected",
            }
        )

    async def call_rejected(self, event):
        await self.send(text_data=json.dumps({
            "action": "call_rejected",
        }))

    async def forward_signal(self, data, action):
        target_id = data.get("target_user") or data.get("caller_id")
        await self.channel_layer.group_send(
            f"user_{target_id}",
            {"type": action, **data}
        )

    async def offer(self, event):
        await self.send(text_data=json.dumps(event))

    async def answer(self, event):
        await self.send(text_data=json.dumps(event))

    async def ice_candidate(self, event):
        await self.send(text_data=json.dumps(event))
