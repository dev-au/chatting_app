from datetime import datetime
from enum import Enum
from typing import TypeVar

from tortoise import fields, Model

Self = TypeVar('Self', bound='User')


class UserStatus(Enum):
    ONLINE = 'Online'
    OFFLINE = str(datetime.now())


class MessageDirection(Enum):
    SENT = 'sent'
    RECEIVED = 'received'


class User(Model):
    username = fields.CharField(max_length=15, primary_key=True)
    fullname = fields.CharField(max_length=50)
    password = fields.TextField()
    status = fields.CharEnumField(UserStatus, default=UserStatus.ONLINE)

    async def get_connections(self):
        all_messages = await Message.filter(sender=self)
        users = []
        for message in all_messages:
            users.append(message.receiver)
        return users

    async def get_chat_history(self):
        all_sent_messages = await self.filter(sender=self)
        all_received_messages = await self.filter(receiver=self)
        all_messages = all_sent_messages + all_received_messages
        history = sorted(all_messages, key=lambda x: x.timestamp)
        return history

    async def update_status(self, online=False, offline=False):
        if online:
            return await self.update_from_dict({'status': UserStatus.ONLINE})
        elif offline:
            return await self.update_from_dict({'status': UserStatus.OFFLINE})
        raise ValueError('You must give online or offline')

    async def read_all_messages(self, sender: Self):
        await Message.filter(sender=sender, receiver=self).update(is_read=True)


class Message(Model):
    sender = fields.ForeignKeyField('models.User', related_name='sent_messages')
    receiver = fields.ForeignKeyField('models.User', related_name='received_messages')
    content = fields.TextField()
    timestamp = fields.DatetimeField(auto_now_add=True)
    is_read = fields.BooleanField(default=False)
