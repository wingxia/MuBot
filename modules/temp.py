from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.message.parser.base import MatchTemplate
from graia.ariadne.model import Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from function.small_tool import get_img_id

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        decorators=[MatchTemplate([Plain("id"), Image])],
    )
)
async def send_img_id(app: Ariadne, message: MessageChain, friend: Friend):
    img_id = get_img_id(message)
    await app.send_friend_message(friend, MessageChain.create(Plain(img_id)))
