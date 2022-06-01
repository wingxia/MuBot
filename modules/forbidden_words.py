from function.rsql import run_sql
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Image, Plain
from graia.ariadne.model import Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()

forbiddingWords = run_sql(f"select fbword from fbwords")


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def forbidden_words(app: Ariadne, group: Group, message: MessageChain, member: Member):
    for forbiddenWord in forbiddingWords:
        if forbiddenWord in message.asDisplay():
            fb_c = run_sql(f"select * from fbowrds where words = '{forbiddenWord}'")
            if group.id in fb_c[3] or fb_c[0]:
                await app.recallMessage(source)
                await app.muteMember(group, member, fb_c[2])
                await app.sendGroupMessage(group, MessageChain.create(
                    At(member), Plain(f"！欢迎进入小黑屋，以后可不要来了。\n触发违禁词'{forbiddenWord}'")
                ))
