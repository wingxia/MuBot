import hashlib,base64

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
    my_md5.update(context)  # 得到MD5消息摘要
    hash_value = my_md5.hexdigest()  # 以16进制返回消息摘要，32位
    return hash_value


def element_str_to_msg_chain(element_str):
    if element_str.find('[mirai:') == -1:
        return MessageChain(Plain(f"{element_str}"))
    type_st_index = element_str.find('mirai:') + 6
    type_end_index = element_str.find(':', type_st_index)  # 切片找到element类型
    element_type = element_str[type_st_index:type_end_index]  # 服了，要长时间保存消息，就保存成好用的样子啊。摸出来用这么麻烦。
    match element_type:
        case 'Image' | 'Voice':
            base64_data_st = element_str.find('"base64":"') + 10
            base64_data_end = element_str.find('"', base64_data_st)
            base64_data = element_str[base64_data_st:base64_data_end]  # 获取base64编码
            img_data = base64.b64decode(base64_data)
            md5 = get_md5_value(img_data)
            match element_type:
                case 'Image':
                    file_data = open(f'..\\data\\imgs\\{md5}.jpg', "wb")
                case 'Voice':
                    file_data = open(f'..\\data\\imgs\\{md5}.amr', "wb")
            # noinspection PyUnboundLocalVariable
            file_data.write(img_data)
            file_data.close()
            match element_type:
                case 'Image':
                    msg_chain = f'MessageChain(Image(ata_bytes=Path("data", "imgs", f"{md5}.jpg").read_bytes()))'
                case 'Voice':
                    msg_chain = f'MessageChain(Image(ata_bytes=Path("data", "imgs", f"{md5}.amr").read_bytes()))'
            # noinspection PyUnboundLocalVariable
            return msg_chain


Gvb.msg_element_list = []
Gvb.end_tz = 0


def str_find_element(str_data, start_index=0):  # 输入长期储存的消息链，返回每一个元素的索引到全局变量
    start_tz = str_data.find('[mirai:', start_index)
    if start_tz == -1:
        Gvb.msg_element_list.append([start_index, len(str_data)])
        return None
    if start_tz != Gvb.end_tz:
        Gvb.msg_element_list.append([Gvb.end_tz, start_tz])
    Gvb.end_tz = str_data.find(']', start_tz) + 1
    Gvb.msg_element_list.append([start_tz, Gvb.end_tz])
    if Gvb.end_tz == len(str_data):
        return None
    str_find_element(str_data, Gvb.end_tz)
