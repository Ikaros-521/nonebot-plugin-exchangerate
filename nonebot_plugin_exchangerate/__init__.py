import contextlib
from typing import Any, Dict

from nonebot import on_endswith, on_fullmatch, on_regex
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import RegexDict
#from nonebot.params import Endswith
#from nonebot.log import logger

from .exchangerate import exchange_currency, get_currency_info, get_currency_list

exchange = on_regex(r"(?P<amount>^\d+\.?\d*)(?P<currency>[\u4e00-\u9fff]{1,5}$)")


@exchange.handle()
async def _(matched: Dict[str, Any] = RegexDict()) -> None:
    with contextlib.suppress(ValueError):
        total = exchange_currency(matched["currency"], float(matched["amount"]))
        msg = f"{total}人民币"
        if total != "查找的货币不存在":
            await exchange.send(msg, reply_message=True)


info = on_endswith("汇率")


@info.handle()
async def _(event: MessageEvent) -> None:
    txt = event.get_plaintext()
    try:
        currency = txt[: len(txt) - 2]
        if len(currency) > 5:
            return
        msg = get_currency_info(currency)
    except ValueError as e:
        msg: str = str(e)
    await info.send(msg)


statement = on_fullmatch(("货币列表", "汇率列表"))


@statement.handle()
async def _() -> None:
    currency_list = get_currency_list()
    msg = "支持查询的货币:\n" + "\n".join(currency_list)
    await statement.send(msg)
