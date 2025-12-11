from src.strategies.BaseStrategy import BaseStrategy
import backtrader as bt

class SMAStrategy(BaseStrategy):

    params = (('SMA_period', 10),)

    def __init__(self):
        super().__init__()

        self.crossovers = {}
        for d in self.datas:
            sma = bt.indicators.SimpleMovingAverage(d.close, period=self.params.SMA_period)
            self.crossovers[d] = bt.indicators.CrossOver(d.close, sma)

    def next(self):
        super().next()

        for data in self.datas:

            own = self.position(data)
            cross = self.crossovers[data][0]

            if self.orders[data] is not None:
                continue

            # BUY
            if own == 0 and cross > 0:
                self.log(f"BUY SIGNAL {data._name}")
                self.orders[data] = self.buy(data=data)

            # SELL
            elif own > 0 and cross < 0:
                self.log(f"SELL SIGNAL {data._name}")
                self.orders[data] = self.sell(data=data)
