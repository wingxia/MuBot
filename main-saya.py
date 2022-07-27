import asyncio
import pkgutil

from graia.saya import Saya
from graia.ariadne import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.broadcast import Broadcast
from graia.saya.builtins.broadcast import BroadcastBehaviour

loop = asyncio.new_event_loop()
bcc = Broadcast(loop=loop)
Ariadne.config(loop=loop, broadcast=bcc)
app = Ariadne(
    connection=config(
        1691641,  # 你的机器人的 qq 号
        "wingxiaismydad",  # 填入 verifyKey
        # 以下两行是你的 mirai-api-http 地址中的地址与端口
        # 默认为 "http://localhost:8080" 如果你没有改动可以省略这两行
        HttpClientConfig(host="http://10.144.17.0:2002"),
        WebsocketClientConfig(host="http://10.144.17.0:2002"),
    ),
)
saya = app.create(Saya)
saya.install_behaviours(
    app.create(BroadcastBehaviour),
)

with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            continue
        print(module_info, module_info.name)
        saya.require("modules." + module_info.name)

app.launch_blocking()
