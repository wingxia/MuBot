from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage,FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Image, Plain
from graia.ariadne.model import Group, Member, MemberPerm
from graia.ariadne.message.parser.twilight import FullMatch, Twilight, RegexMatch, ElementMatch
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from function.small_tool import get_img_id

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        # inline_dispatchers=[Twilight(ElementMatch(Image))]
    )
)
async def send_img_id(app: Ariadne,message: MessageChain):
    message.asPersistentString()
    # print(message.asPersistentString())
    # img_id = get_img_id(pr_message)
    # await app.sendGroupMessage(group, MessageChain.create(Plain(img_id)))
