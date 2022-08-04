import asyncio
import os
from pathlib import Path

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import *
from graia.ariadne.message.parser.twilight import Twilight, RegexMatch
from graia.ariadne.model import Group, Member, MemberPerm
from graia.broadcast.interrupt import InterruptControl
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast import ListenerSchema

from function.GlobalVariable import globalVariables as Gvb
from function.rsql import run_sql
from function.small_tool import MessageWaiter, msg_str_to_file, fresh_cache

saya = Saya.current()
channel = Channel.current()
inc = InterruptControl(saya.broadcast)  # type: ignore
Gvb.AdminList = run_sql("select qq_id from admin")
Gvb.KeyWordsList = run_sql("select keywords from keywords_reply")
MessageChain(At(666), Image(data_bytes=Path("data", "imgs", "graiax.png").read_bytes()),
             Plain("wer"))  # 别再把我的导入优化掉了，我要用！！！


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def keywords_reply(app: Ariadne, group: Group, message: MessageChain):
    for word in Gvb.KeyWordsList:  # 遍历每个关键词
        if word in message:  # 关键词命中消息
            reply_c = run_sql(f"select * from keywords_reply where keywords = '{word}'order by `group` LIMIT 1")  # 获取关键词回复配置
            re_chain = MessageChain.from_persistent_string(open(reply_c[3], 'r').read())
            if reply_c[1] == group.id or reply_c[1] == 0:  # 在作用群内
                if message.display == word:  # 消息等于关键词，直接发送
                    await app.send_group_message(group, re_chain)
                    break
                elif reply_c[2]:  # 不相等且精准匹配
                    pass
                else:  # 不相等，模糊匹配
                    await app.send_group_message(group, re_chain)
                    break


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight(RegexMatch(r"添加全局回复词.*|添加回复词.*"))]
    )
)
async def ero(app: Ariadne, group: Group, message: MessageChain, member: Member):
    message_str = message.as_display().replace(" ", "")
    if message_str.startswith('添加回复词'):
        if member.permission != MemberPerm.Member:

            reply_key = message_str[5:]
            try:
                await app.send_group_message(group, MessageChain([f"请发送关键词'{reply_key}'的回复消息"]))
                ret_msg = await inc.wait(MessageWaiter(group, member), timeout=20)  # 强烈建议设置超时时间否则将可能会永远等待
            except asyncio.TimeoutError:
                await app.send_message(group, MessageChain([Plain("你说话了吗？")]))
            else:
                await app.send_group_message(group, MessageChain(['正在处理中。。。']))
                msg_str = ret_msg.as_persistent_string()
                file_dir = msg_str_to_file(msg_str)
                if not run_sql(
                        f"select * from keywords_reply where keywords='{reply_key}' and `group`={group.id}"):  # 如果该关键词没有记录
                    run_sql(f"insert into keywords_reply values ('{reply_key}',{group.id},1,'{file_dir}')")
                    await app.send_group_message(group, MessageChain('处理完成，记录已添加'))
                    fresh_cache()
                else:
                    run_sql(
                        f"update keywords_reply set chain_file_dir='{file_dir}' where `group` = {group.id} and keywords='{reply_key}'")
                    await app.send_group_message(group, MessageChain('该关键词存在记录，已覆盖'))
        else:
            await app.send_group_message(group, MessageChain(f"添加回复词操作需要管理员权限"))

    if message_str.startswith('添加全局回复词'):  # ----------------全局配置----------------------
        if member.id in Gvb.AdminList:
            message_str = message_str.replace(" ", "")
            reply_key = message_str[7:]
            try:
                await app.send_group_message(group, MessageChain([f"请发送全局词'{reply_key}'的回复消息"]))
                ret_msg = await inc.wait(MessageWaiter(group, member), timeout=20)  # 强烈建议设置超时时间否则将可能会永远等待
            except asyncio.TimeoutError:
                await app.send_message(group, MessageChain([Plain("你说话了吗？")]))
            else:
                await app.send_group_message(group, MessageChain(['正在处理中。。。']))
                msg_str = ret_msg.as_persistent_string()
                file_dir = msg_str_to_file(msg_str)
                if not run_sql(
                        f"select * from keywords_reply where keywords='{reply_key}' and `group`=0"):  # 如果该关键词没有记录
                    run_sql(f"insert into keywords_reply values ('{reply_key}',0,1,'{file_dir}')")
                    await app.send_group_message(group, MessageChain('处理完成，全局记录已添加'))
                    fresh_cache()
                else:
                    run_sql(
                        f"update keywords_reply set chain_file_dir='{file_dir}'where `group` = 0 and keywords='{reply_key}'")
                    await app.send_group_message(group, MessageChain('该全局回复词存在记录，已覆盖'))
        else:
            await app.send_group_message(group, MessageChain(f"全局配置需要超管权限，卡BUG呢"))
