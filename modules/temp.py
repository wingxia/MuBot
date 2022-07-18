from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.twilight import Twilight, FullMatch
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

from function.small_tool import fresh_cache

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage],
                            inline_dispatchers=[
                                Twilight(FullMatch("刷新缓存"), )]
                            ))
async def hello(app: Ariadne, target: Union[GroupMessage, FriendMessage]):
    try:
        fresh_cache()
    except Exception as e:
        await app.send_message(target, MessageChain(f'发生异常{e}'))
    else:
        await app.send_message(target, MessageChain(f'缓存已刷新'))
