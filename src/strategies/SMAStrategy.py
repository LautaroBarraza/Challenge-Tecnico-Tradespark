
import src.strategies.BaseStrategy as BaseStrategy

import backtrader as bt

class GoldenCrossStrategy(BaseStrategy):

    params= (
        ('SMA_period', 10),
    )

    def __init__(self):
        # Define the short and long moving averages
        self.sma= bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.SMA_period)