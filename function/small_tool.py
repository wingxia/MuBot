import hashlib
import os

from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import *
from graia.ariadne.model import Group, Member
from graia.broadcast.interrupt import Waiter

from function.GlobalVariable import globalVariables as Gvb
from function.rsql import run_sql


def get_img_id(message: MessageChain):
    pr_str = message.as_persistent_string()
    id_index = pr_str.find('imageId') + 10
    return pr_str[id_index:id_index + 42]


def fresh_cache():
    Gvb.skyDealGroups = run_sql("select group_id from group_sw where deal = 1")
    Gvb.forbiddingWords = run_sql(f"select words from fb_words")
    Gvb.KeyWordsList = run_sql("select keywords from keywords_reply")
    Gvb.AdminList = run_sql("select qq_id from admin")


# noinspection PyMethodOverriding
class MessageWaiter(Waiter.create([GroupMessage])):
    """Next Message接收器"""

    def __init__(self, group: Union[Group, int], member: Union[Member, int]):
        self.group = group if isinstance(group, int) else group.id
        self.member = member if isinstance(member, int) else member.id

    async def detected_event(self, group: Group, member: Member, message: MessageChain):
        if self.group == group.id and self.member == member.id:
            return message


def get_md5_value(context):
    my_md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
    my_md5.update(context.encode('utf-8'))  # 得到MD5消息摘要
    hash_value = my_md5.hexdigest()  # 以16进制返回消息摘要，32位
    return hash_value


def msg_str_to_file(message_str: str):
    md5 = get_md5_value(message_str)
    print(os.getcwd())
    file_data = open(f"data\\message_str\\{md5}.txt", "w+")
    file_data.write(message_str)
    file_data.close()
    return f"data\\\message_str\\\{md5}.txt"
