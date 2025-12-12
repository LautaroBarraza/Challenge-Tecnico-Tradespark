from src.strategies.BaseStrategy import BaseStrategy
import backtrader as bt

class GoldenCrossStrategy(BaseStrategy):

    """
    Golden Cross Strategy
    This strategy buys when the short-term SMA crosses above the long-term SMA (Golden Cross)
    and sells when the short-term SMA crosses below the long-term SMA (Death Cross).
    :param SMA_short_period: Period for the short-term Simple Moving Average.
    :param SMA_long_period: Period for the long-term Simple Moving Average.
    """

    params = (
        ('SMA_short_period', 10),
        ('SMA_long_period', 30)
    )

    def __init__(self):
        super().__init__()
        self.crossovers = {}
        for d in self.datas:
            sma_s = bt.indicators.SimpleMovingAverage(d.close, period=self.params.SMA_short_period)
            sma_l = bt.indicators.SimpleMovingAverage(d.close, period=self.params.SMA_long_period)
            self.crossovers[d] = bt.indicators.CrossOver(sma_s, sma_l)

    def next(self):
        super().next()

        for data in self.datas:

            own = self.position(data)
            cross = self.crossovers[data][0]

            if self.orders[data] is not None:
                continue

            if own == 0 and cross > 0:
                self.log(f"GOLDEN CROSS BUY {data._name}")
                self.orders[data] = self.buy(data=data)

            elif own > 0 and cross < 0:
                self.log(f"GOLDEN CROSS SELL {data._name}")
                self.orders[data] = self.sell(data=data)
