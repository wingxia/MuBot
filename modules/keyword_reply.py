from function.rsql import run_sql
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Image, Plain
from graia.ariadne.model import Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()

KeyWordsList = run_sql("select keywords from keywords_reply")
MessageChain.create(At(666), Image(), Plain("wer"))  # 别再把我的导入优化掉了，我要用！！！


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def keywords_reply(app: Ariadne, group: Group, message: MessageChain, member: Member):
    for word in KeyWordsList:  # 遍历每个关键词
        if word in message:  # 关键词命中消息
            reply_c = run_sql(f"select * from keywords_reply where keywords = '{word}'")  # 获取关键词回复配置
            re_chain = MessageChain.create(reply_c[3])
            print(reply_c)
            for i in range(4, len(reply_c)):
                exec("re_chain.append(" + reply_c[i] + ")")
            print(re_chain)
            if reply_c[1] == group.id or reply_c[1] == 0:  # 在作用群内
                if message.display == word:  # 消息等于关键词，直接发送
                    await app.send_group_message(group, re_chain)
                    break
                elif reply_c[2]:  # 不相等且精准匹配
                    break
                else:  # 不相等，模糊匹配
                    await app.send_group_message(group, re_chain)
                    break


