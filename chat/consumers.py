import json
from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async, async_to_sync

from chat.models import Room, Member


def create_room(name, channel_name):
    ''' Create new room record in the db if it does not exist'''
    room, created = Room.objects.get_or_create(name=name,
                                               defaults={'name': name, 'channel_name': channel_name})
    return room


def add_member(room, user):
    Member.objects.get_or_create(room=room, user=user)


def get_members(room):
    members = Member.objects.filter(room=room)
    return [member.user.username for member in members]


def remove_member(room, user):
    members = Member.objects.filter(room=room).filter(user=user).delete()


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            self.room = await sync_to_async(create_room)(self.room_name, self.channel_name)
            await sync_to_async(add_member)(self.room, self.scope['user'])
            members = await sync_to_async(get_members)(self.room)

            # broadcast to all the current members that new member has joined
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chatroom_joined', 'message_type': 'joined',
                    'username': self.scope['user'].username,
                }
            )
            # send the current list of members to the new member
            await self.send(json.dumps({'type': 'chatroom_members',
                                        'message':  members}))
            print(self.channel_name, 'all good?')
        except:
            import traceback
            traceback.print_exc()
            raise

    async def disconnect(self, close_code):
        try:
            print(self.channel_name, "disconnected")

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chatroom_left',
                    'username': self.scope['user'].username,
                }
            )
            await sync_to_async(remove_member)(self.room, self.scope['user'])

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except:

            import traceback
            traceback.print_exc()
            raise

    async def chatroom_joined(self, event):
        try:
            if event['username'] != self.scope['user'].username:
                username = event['username']

                await self.send(text_data=json.dumps({
                    'type': 'chatroom_joined',
                    'username': username,
                }))
        except:
            import traceback
            traceback.print_exc()
            raise

    async def chatroom_left(self, event):
        try:
            print('LEFT MESSAGE')
            username = event['username']

            await self.send(text_data=json.dumps({
                'type': 'chatroom_left',
                'username': username,
            }))
        except:
            import traceback
            traceback.print_exc()
            raise

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username = text_data_json['username']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chatroom_message',

                    'message': message,
                    'username': username,
                }
            )
        except:
            print('error')
            import traceback
            traceback.print_exc()
            raise

    async def chatroom_message(self, event):
        try:
            username = event['username']
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'type': 'chatroom_message',
                'username': username,
            }))
        except:
            import traceback
            traceback.print_exc()
            raise

    pass
