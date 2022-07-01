from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.message.parser.base import MatchTemplate
from graia.ariadne.model import Friend, Member, Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from function.small_tool import get_img_id
from function.rsql import run_sql

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        decorators=[MatchTemplate([Plain("id"), Image])],
    )
)
async def send_img_id(app: Ariadne, message: MessageChain, friend: Friend):  # 返回图片id
    img_id = get_img_id(message)
    await app.send_friend_message(friend, MessageChain.create(Plain(img_id)))


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MatchTemplate([Plain("设置含义"), Plain, Image])],
    )
)
async def send_img_id(app: Ariadne, message: MessageChain, member: Member, group: Group):  # 记录图片含义
    if member.id in [1845764432] and group.id == 836217084:
        img_id = get_img_id(message)
        message_str = str(message).replace(" ", "")
        run_sql(f"insert into image(imgId,note) values ('{img_id}','{message_str[4:-4]}')")
        sql_em = run_sql(f"select * from image where imgId='{img_id}'")
        if sql_em:
            await app.send_group_message(group, MessageChain.create(Plain(f"设置成功!\n记录值为{sql_em}")))
