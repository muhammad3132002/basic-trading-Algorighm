from collections import namedtuple

import numpy as np
import talib

from jesse.helpers import get_candle_source
from jesse.helpers import get_config

KST = namedtuple('KST', ['line', 'signal'])


def kst(candles: np.ndarray, sma_period1: int = 10, sma_period2: int = 10, sma_period3: int = 10, sma_period4: int = 15,
        roc_period1: int = 10, roc_period2: int = 15, roc_period3: int = 20, roc_period4: int = 30,
        signal_period: int = 9, source_type: str = "close", sequential: bool = False) -> KST:
    """
    Know Sure Thing (KST)

    :param candles: np.ndarray
    :param sma_period1: int - default=10
    :param sma_period2: int - default=10
    :param sma_period3: int - default=10
    :param sma_period4: int - default=15
    :param roc_period1: int - default=10
    :param roc_period2: int - default=15
    :param roc_period3: int - default=20
    :param roc_period4: int - default=30
    :param signal_period: int - default=9
    :param source_type: str - default: "close"
    :param sequential: bool - default=False

    :return: KST(line, signal)
    """
    warmup_candles_num = get_config('env.data.warmup_candles_num', 240)
    if not sequential and len(candles) > warmup_candles_num:
        candles = candles[-warmup_candles_num:]

    source = get_candle_source(candles, source_type=source_type)

    aroc1 = talib.SMA(talib.ROC(source, timeperiod=roc_period1), sma_period1)
    aroc2 = talib.SMA(talib.ROC(source, timeperiod=roc_period2), sma_period2)
    aroc3 = talib.SMA(talib.ROC(source, timeperiod=roc_period3), sma_period3)
    aroc4 = talib.SMA(talib.ROC(source, timeperiod=roc_period4), sma_period4)
    line = aroc1[len(aroc1) - len(aroc4):] + 2 * aroc2[len(aroc2) - len(aroc4):] + \
           3 * aroc3[len(aroc3) - len(aroc4):] + 4 * aroc4
    signal = talib.SMA(line, signal_period)

    if sequential:
        return KST(line, signal)
    else:
        return KST(line[-1], signal[-1])
