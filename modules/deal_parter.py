import asyncio

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Plain, AtAll
from graia.ariadne.message.parser.base import MatchTemplate
from graia.ariadne.model import Group, Member, MemberPerm
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

from function.rsql import run_sql
from function.small_tool import get_img_id

channel = Channel.current()

skyDealGroups = [499949933, 836217084]


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def deal_parter(app: Ariadne, group: Group, message: MessageChain, member: Member):  # 文字控制
    if group.id in skyDealGroups:
        if member.permission != MemberPerm.Member:
            if message.display in ['有单', '全体禁言', '板选', '全禁', '嘘～', '嘘~']:
                await app.mute_all(group)
            elif message.display in ['恭喜', '解全体禁言', '解除全体禁言', '解禁', '开始报价']:
                await app.unmute_all(group)
            elif message.display == '开始报价':
                await app.unmute_all(group)
                await app.send_group_message(group, MessageChain.create(AtAll()))

            for fuzzyDealKeyword in ['底价：', '底价:', '🈲压价🈲闲聊🈲重复报价']:
                if fuzzyDealKeyword in message.display:
                    await app.mute_all(group)
                    await app.send_group_message(group,
                                                 MessageChain.create(AtAll(),
                                                                     Plain(f"啊~哈哈哈，鸡汤来咯~，请认真看完要求再报价(20秒后解除全体禁言)")))
                    await asyncio.sleep(20)
                    await app.unmute_all(group)
                    break


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MatchTemplate([Image])],
    )
)
async def send_img_id(app: Ariadne, member: Member, message: MessageChain, group: Group):  # 返回图片id
    if group.id in skyDealGroups:
        if member.permission != MemberPerm.Member:
            image_id = get_img_id(message)
            img_note = run_sql(f"select note from image where imgId='{image_id}'")[0]
            print(img_note)
            match img_note:
                case '开始报价':
                    await app.send_group_message(group, MessageChain.create(AtAll()))
                    await app.unmute_all(group)
                case '恭喜':
                    await app.unmute_all(group)
                case '板选' | '有单':
                    await app.mute_all(group)
