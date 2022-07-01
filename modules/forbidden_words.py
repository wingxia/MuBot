from function.rsql import run_sql
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Image, Plain, Source
from graia.ariadne.model import Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
import pypinyin

channel = Channel.current()

forbiddingWords = run_sql(f"select words from fb_words")


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def forbidden_words(app: Ariadne, source: Source, group: Group, message: MessageChain, member: Member):
    for forbiddenWord in forbiddingWords:
        if forbiddenWord in message.display:
            fb_c = run_sql(f"select * from fb_words where words = '{forbiddenWord}'")
            if fb_c[2] or group.id in fb_c[2]:
                await app.recall_message(source)
                await app.mute_member(group, member, int(fb_c[1]))
                print(fb_c[1])
                fb_pinyin = pypinyin.pinyin(f"{forbiddenWord}")
                await app.send_group_message(group, MessageChain.create(
                    At(member), Plain(f"！欢迎进入小黑屋，以后可不要来了。\n触发违禁词'{fb_pinyin}'")
                ))
