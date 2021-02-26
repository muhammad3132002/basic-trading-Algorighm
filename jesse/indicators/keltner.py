from collections import namedtuple

import numpy as np
import talib

from jesse.helpers import get_candle_source
from jesse.helpers import get_config

KeltnerChannel = namedtuple('KeltnerChannel', ['upperband', 'middleband', 'lowerband'])


def keltner(candles: np.ndarray, period: int = 20, multiplier: float = 2, matype: int = 1, source_type: str = "close",
            sequential: bool = False) -> KeltnerChannel:
    """
    Keltner Channels

    :param candles: np.ndarray
    :param period: int - default: 20
    :param multiplier: int - default: 2
    :param matype: int - default: 1
    :param source_type: str - default: "close"
    :param sequential: bool - default=False

    :return: KeltnerChannel(upperband, middleband, lowerband)
    """

    warmup_candles_num = get_config('env.data.warmup_candles_num', 240)
    if not sequential and len(candles) > warmup_candles_num:
        candles = candles[-warmup_candles_num:]

    source = get_candle_source(candles, source_type=source_type)
    e = talib.MA(source, timeperiod=period, matype=matype)
    a = talib.ATR(candles[:, 3], candles[:, 4], candles[:, 2], timeperiod=period)

    up = e + a * multiplier
    mid = e
    low = e - a * multiplier

    if sequential:
        return KeltnerChannel(up, mid, low)
    else:
        return KeltnerChannel(up[-1], mid[-1], low[-1])