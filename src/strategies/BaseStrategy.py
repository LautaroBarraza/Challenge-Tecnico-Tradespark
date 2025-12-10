import backtrader as bt

class BaseStrategy(bt.strategy):
    def log(self, txt, dt=None):
        """ Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} , {txt}')
    
    def notify_order(self, order):
        stock= order.data  # Get the ticket name from the data feed

        if order.status in [order.Submitted, order.Accepted]:
            return  # Order is still pending

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm {order.executed.comm:.2f}')
            else:  # Sell
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm {order.executed.comm:.2f}')

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.orders[stock] = None  # Reset orders