import backtrader as bt
import math

class StrategyPercentSizer(bt.Sizer):

    """
    Strategy Percent Sizer
    This sizer allocates a fixed percentage of the portfolio value to each trade.
    :param percents: Percentage of the portfolio to allocate per trade.
    """

    params = (
        ('percents', 10), 
    )

    def _getsizing(self, comminfo, cash, data, isbuy):
        """Determine the size of the order based on a percentage of the portfolio value.
         :param comminfo: Commission info.
         :param cash: Available cash.
         :param data: The data feed (stock).
         :param isbuy: Boolean indicating if the order is a buy or sell.
         :return: Size of the order.
    """
        
        strat = self.strategy

        price= data.close[0]


        if isbuy:
            portfolio_value = strat.broker.getvalue()
            allocated_cash = (self.params.percents / 100) * portfolio_value

            if price <= 0:
                return 0
            
            size = math.floor(allocated_cash / price)

            if size * price > strat.broker.getcash():
                return 0
            
            return size
        else:
            position = strat.position(data)

            if position <= 0:
                return 0
            
            return position
