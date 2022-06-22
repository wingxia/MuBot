from function.rsql import run_sql
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Image, Plain, Source
from graia.ariadne.model import Group, Member, MemberPerm
from graia.ariadne.message.parser.twilight import FullMatch, Twilight, RegexMatch
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from function.rsql import run_sql

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight(RegexMatch(r"我要头衔.*"))]
    )
)
async def special_title(app: Ariadne, group: Group, message: MessageChain, member: Member):
    special_content = message.asDisplay()[4:]
    if len(special_content) <= 6:
        if not run_sql(f"select * from special_title where qqid = {member.id} and groupid = {group.id}"):
            run_sql(
                f"insert into special_title(qqid,specialtitle,groupid) values ({member.id},'{special_content}',{group.id})")
            await app.sendGroupMessage(group,
                                       message.create(At(member), f"你在群({group.id})的头衔({special_content})已成功申请请耐心等候~"))
        else:
            run_sql(
                f"update special_title set specialtitle = '{special_content}' where qqid = {member.id} and groupid = {group.id}")
            await app.sendGroupMessage(group,
                                       message.create(At(member),
                                                      f"已在群({group.id})存在头衔申请，已将头衔内容覆盖为({special_content})"))
    else:
        await app.sendGroupMessage(group, MessageChain.create(At(member), "头衔内容太长啦，请不要超过6个字符哦~"))
