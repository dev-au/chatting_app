from fastapi import WebSocket

from data.models import User, Message

online_users = {}


class Chat:
    websocket: WebSocket
    user: User

    def __init__(self, websocket: WebSocket, user: User):
        self.websocket = websocket
        self.user = user

    async def __aenter__(self):
        await self.user.update_status(online=True)
        await self.websocket.accept()
        online_users[self.user.username] = self
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.user.update_status(offline=True)
        await self.websocket.close()

    async def get_connections(self):
        all_chats = await self.user.get_connections()
        await self.websocket.send_json(all_chats)

    async def __upload_message__(self, sender: User, message: Message):
        await self.websocket.send_json(
            {
                "user": sender.username,
                "signal": "message",
                "content": message.content,
                "timestamp": str(message.timestamp),
            }
        )

    async def __upload_action__(self, sender: User, action: str):
        await self.websocket.send_json(
            {
                "user": sender.username,
                "signal": "action",
                "action": action,
            }
        )

    async def read_all_messages(self, sender: User):
        await self.user.read_all_messages(sender)

    async def on_message(self, data):
        username = data['user']
        receiver = await User.get(username=username)
        receiver_socket: Chat = online_users.get(username)
        message = await Message.create(sender=self.user, receiver=receiver, content=data['content'])
        if receiver_socket:
            await receiver_socket.__upload_message__(self.user, message)

    async def on_action(self, data):
        username = data['user']
        receiver_socket: Chat = online_users.get(username)
        if receiver_socket:
            await receiver_socket.__upload_action__(self.user, data['action'])

    async def run_handler(self):
        while True:
            data = await self.websocket.receive_json()
            if data["signal"] == "message":
                await self.on_message(data)
            elif data["signal"] == "action":
                await self.on_action(data)
