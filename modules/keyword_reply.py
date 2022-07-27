import asyncio
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
from function.small_tool import MessageWaiter, str_find_element, element_str_to_msg_chain

global reply_c
saya = Saya.current()
channel = Channel.current()
inc = InterruptControl(saya.broadcast)  # type: ignore

Gvb.KeyWordsList = run_sql("select keywords from keywords_reply")
MessageChain(At(666), Image(data_bytes=Path("data", "imgs", "graiax.png").read_bytes()),
             Plain("wer"))  # 别再把我的导入优化掉了，我要用！！！


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def keywords_reply(app: Ariadne, group: Group, member: Member, message: MessageChain):
    for word in Gvb.KeyWordsList:  # 遍历每个关键词
        if word in message:  # 关键词命中消息
            global reply_c
            reply_c = run_sql(f"select * from keywords_reply where keywords = '{word}'")  # 获取关键词回复配置
            exec(f're_chain = {MessageChain(reply_c[3])}', globals())
            if len(reply_c) > 4:
                for i in range(4, len(reply_c)):
                    exec(f"re_chain+={reply_c[i]}", globals())
            if reply_c[1] == group.id or reply_c[1] == 0:  # 在作用群内
                if message.display == word:  # 消息等于关键词，直接发送
                    await app.send_group_message(group, re_chain)
                    break
                elif reply_c[2]:  # 不相等且精准匹配
                    break
                else:  # 不相等，模糊匹配
                    await app.send_group_message(group, re_chain)
                    break


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight(RegexMatch(r"添加全局回复关键词.*|添加回复关键词.*"))]
    )
)
async def ero(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if member.permission != MemberPerm.Member:
        message_str = message.as_display()
        if message_str.startswith('添加回复关键词'):
            message_str.replace(' ', '')
            reply_key = message_str[7:]
            try:
                await app.send_group_message(group, MessageChain([f"请发送关键词'{reply_key}'的回复消息"]))
                ret_msg = await inc.wait(MessageWaiter(group, member), timeout=20)  # 强烈建议设置超时时间否则将可能会永远等待
            except asyncio.TimeoutError:
                await app.send_message(group, MessageChain([Plain("你说话了吗？")]))
            else:
                await app.send_group_message(group, MessageChain(['正在处理中。。。']))
                d_binary = await message.download_binary()
                print(f'download_binary={d_binary}')
                msg_str = ret_msg.as_persistent_string()

                str_find_element(msg_str)
                elements_index = Gvb.msg_element_list
                Gvb.rm('msg_element_list')
                chain_list = []
                for e_index in elements_index:
                    print(msg_str[e_index[0]:e_index[1]])
                    chain_list.append(element_str_to_msg_chain(msg_str[e_index[0]:e_index[1]]))
                chain_list_len = len(chain_list)
                if chain_list_len < 6:
                    for i in range(0, 6 - chain_list_len):
                        chain_list.append('null')
                str_chain_list = str(chain_list)
                str_chain_list.replace('[', '').replace(']', '').replace("'null'", "")
                sql_return = run_sql(f"insert into keywords_reply values ('{reply_key}',{group.id},1,)")
                print(sql_return)
                await app.send_group_message(group, MessageChain(sql_return))
