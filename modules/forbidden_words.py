import pypinyin
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Plain, Source
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Group, Member, MemberPerm
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from function.GlobalVariable import globalVariables as Gvb
from function.rsql import run_sql
from function.small_tool import fresh_cache

channel = Channel.current()
Gvb.forbiddingWords = run_sql(f"select words from fb_words")


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def forbidden_words(app: Ariadne, source: Source, group: Group, message: MessageChain, member: Member):
    for forbiddenWord in Gvb.forbiddingWords:
        if forbiddenWord in message.display:
            fb_c = run_sql(f"select * from fb_words where words = '{forbiddenWord}' and act_on = 1 limit 1")
            if not fb_c:
                fb_c = run_sql(
                    f"select * from fb_words where words = '{forbiddenWord}' and act_on = {group.id} limit 1")
                if not fb_c:
                    break
            if (fb_c[2]) == 1 or (group.id == fb_c[2]):
                await app.recall_message(source)
                await app.mute_member(group, member, int(fb_c[1]))
                fb_pinyin = pypinyin.pinyin(f"{forbiddenWord}")
                await app.send_group_message(group, MessageChain(
                    At(member), Plain(f"！欢迎进入小黑屋，以后可不要来了。\n触发违禁词'{fb_pinyin}'")
                ))


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[DetectPrefix("添加违禁词")],
    )
)
async def add_group_forbidden_word(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if member.permission != MemberPerm.Member:
        forb_c = message.display[5:].split()
        # noinspection PyTypeChecker
        forb_c[1] = int(forb_c[1])
        if len(forb_c) == 2 and type(forb_c[0]) == str and type(int(forb_c[1])) == int:
            if not run_sql(f"select * from fb_words where words ='{forb_c[0]}' and act_on={group.id}"):
                run_sql(
                    f"insert into fb_words(words,mute_time,act_on) values ('{forb_c[0]}',{forb_c[1] * 60},{group.id})")
                fbw_pinyin = pypinyin.pinyin(f"{forb_c[0]}")
                await app.send_group_message(group, MessageChain(f"违禁词[{fbw_pinyin}]已添加,禁言时间为{forb_c[1]}分钟"))
                fresh_cache()
            else:
                await app.send_group_message(group, MessageChain(f"该违禁词已存在"))
    else:
        await app.send_group_message(group,MessageChain("权限不足：需要管理员权限。"))


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[DetectPrefix("添加全局违禁词")],
    )
)
async def add_globe_forbidden_word(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if member.id in Gvb.AdminList:
        forb_c = message.display[7:].split()
        # noinspection PyTypeChecker
        forb_c[1] = int(forb_c[1])
        if len(forb_c) == 2 and type(forb_c[0]) == str and type(int(forb_c[1])) == int:
            if not run_sql(f"select * from fb_words where words ='{forb_c[0]}' and act_on = 1"):
                run_sql(f"insert into fb_words(words,mute_time,act_on) values ('{forb_c[0]}',{forb_c[1] * 60},1)")
                fbw_pinyin = pypinyin.pinyin(f"{forb_c[0]}")
                await app.send_group_message(group, MessageChain(f"违禁词[{fbw_pinyin}]已添加,禁言时间为{forb_c[1]}分钟"))
                fresh_cache()
            else:
                await app.send_group_message(group, MessageChain(f"全局该违禁词已存在"))
    else:
        await app.send_group_message(group,MessageChain("权限不足：全局配置需要超管权限，你卡BUG呢。"))