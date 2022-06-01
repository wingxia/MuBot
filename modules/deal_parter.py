from function.rsql import run_sql
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Image, Plain
from graia.ariadne.model import Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()

skyGroups = [499949933]


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def deal_parter(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if group.id in skyGroups:
        if member.permission != MemberPerm.Member:
            if message.messageChain.asDisplay() in ['有单', '全体禁言']:
                await app.muteAll(group)
            if message.messageChain.asDisplay() in ['恭喜', '解全体禁言', '解除全体禁言', '开始报价']:
                await app.unmuteAll(group)
            for fuzzyMuteAllKeyword in ['底价：', '底价:']:
                if fuzzyMuteAllKeyword in message.messageChain.asDisplay():
                    await app.muteAll(group)
            if '🈲压价🈲闲聊🈲重复报价' in message.messageChain.asDisplay():
                await app.unmuteAll(group)
