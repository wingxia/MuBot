from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.twilight import Twilight, FullMatch

from graia.saya.builtins.broadcast import ListenerSchema

from function.small_tool import fresh_cache
from function.GlobalVariable import globalVariables as Gvb

fresh_cache()
print(Gvb.AdminList)
