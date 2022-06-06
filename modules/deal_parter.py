from function.rsql import run_sql
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Image, Plain, AtAll
from graia.ariadne.model import Group, Member, MemberPerm
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()

skyGroups = [499949933, 836217084]


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def deal_parter(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if group.id in skyGroups:
        if member.permission != MemberPerm.Member:
            if message.asDisplay() in ['有单', '全体禁言', '全禁', '嘘～', '嘘~']:
                await app.muteAll(group)
            elif message.asDisplay() in ['恭喜', '解全体禁言', '解除全体禁言', '解禁', '开始报价']:
                await app.unmuteAll(group)
            for fuzzyDealKeyword in ['底价：', '底价:', '🈲压价🈲闲聊🈲重复报价']:
                if fuzzyDealKeyword in message.asDisplay():
                    await app.muteAll(group)
                    await app.sendGroupMessage(group,
                                               MessageChain.create(AtAll(), f"啊~哈哈哈，鸡汤来咯~，请认真看完要求再报价(20秒后解除全体禁言)"))
                    await asyncio.sleep(20)
                    await app.unmuteAll(group)
