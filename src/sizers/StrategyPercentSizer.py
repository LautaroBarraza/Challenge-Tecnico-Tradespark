import backtrader as bt
import math

class StrategyPercentSizer(bt.Sizer):
    params = (
        ('percents', 10), 
    )

    def _getsizing(self, comminfo, cash, data, isbuy):
        
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
