
import src.strategies.BaseStrategy as BaseStrategy

import backtrader as bt

class GoldenCrossStrategy(BaseStrategy):

    params= (
        ('SMA_short_period', 10),
        ('SMA_long_period', 30),
    )

    def __init__(self):
        # Define the short and long moving averages
        self.sma_short = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.SMA_short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.SMA_long_period)
        self.crossover = bt.indicators.CrossOver(self.sma_short, self.sma_long)

        operations= []

        ## Initialize a dictionary to keep track of orders for each data feed
        self.orders = {d: None for d in self.datas}



    def next(self):
        for data in self.datas:

            posicion = self.getposition(data).size

            if self.orders[data]: 
                continue

        if señal_compra:
            
            # Check for crossover signals
            if not posicion:  # Not in the market
                if self.crossover > 0:  #buy signal
                    self.log(f'BUY CREATE, {self.data.close[0]:.2f}')
                    self.orders[data] = self.buy(data=data)
            else:  # In the market
                if self.crossover < 0:  # close signal
                    self.log(f'CLOSE CREATE, {self.data.close[0]:.2f}')
                    self.orders[data] = self.close(data=data)