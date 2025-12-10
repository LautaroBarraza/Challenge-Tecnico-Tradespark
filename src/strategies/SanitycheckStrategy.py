import backtrader as bt

class SanityCheckStrategy(bt.Strategy):
    def next(self):
        """
        Simple strategy that prints out the date, closing price, and volume
        for each data feed every 10 bars.
        
        :param self: Strategy instance.
        """
        if len(self) % 10 == 0:
            print(f"Data: {self.data._name} | "
                  f"Fecha: {self.data.datetime.date(0)} | "
                  f"Cierre: {self.data.close[0]:.2f} | "
                  f"Vol: {self.data.volume[0]}")