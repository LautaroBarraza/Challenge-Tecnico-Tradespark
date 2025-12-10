from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import src.config as config
import src.utils.data_loader as data_loader

##strategies
import src.strategies as strategies

import backtrader as bt
import backtrader.sizers as btsizers

if __name__ == '__main__':

    ## Initialize Cerebro engine
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(config.INITIAL_CASH)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    ## Load data and add to Cerebro
    tickets_list = config.STRATEGY_TICKETS
    init_date=config.INIT_DATE
    end_date=config.END_DATE
    for ticket in tickets_list:
        data_loader.load_stock_data(ticket, init_date, end_date)
        data = bt.feeds.GenericCSVData(
            dataname=config.DATA_PATH + f'{ticket}.csv',
            dtformat='%Y-%m-%d', 
            fromdate=datetime.datetime.strptime(init_date, '%Y-%m-%d'),
            todate=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
            datetime=0,
            close=1,  
            high=2,
            low=3,
            open=4,
            volume=5,
            openinterest=-1,
            nullvalue=0.0,
            header=True
        )
        cerebro.adddata(data, name=ticket)


    cerebro.addstrategy(strategies.GoldenCrossStrategy(SMA_short_period=10, SMA_long_period=30))
    cerebro.addstrategy(strategies.SMAStrategy(SMA_period=10))
    cerebro.addstrategy(strategies.SMAStrategy(SMA_period=30))
    cerebro.addsizer(btsizers.PercentSizer, percents=10)
    ## Run Cerebro Engine
    cerebro.run()
    ## Plot results
    cerebro.plot(style='candlestick', open=True)

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())