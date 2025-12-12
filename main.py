from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import pandas as pd


## utils and config
import src.config as config
import src.utils.data_loader as data_loader
import src.utils.strategies_transaction_resume as strategy_transaction_resume  
from src.sizers.StrategyPercentSizer import StrategyPercentSizer

##strategies
from src.strategies.GoldenCrossStrategy import GoldenCrossStrategy
from src.strategies.SMAStrategy import SMAStrategy

import backtrader as bt
import backtrader.sizers as btsizers

if __name__ == '__main__':

    ## Initialize Cerebro engine
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(config.INITIAL_CASH)
    

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    ## Load data and add to Cerebro
    tickers_list = config.STRATEGY_TICKERS
    init_date=config.INIT_DATE
    end_date=config.END_DATE
    for ticker in tickers_list:
        data_loader.load_stock_data(ticker, init_date, end_date)
        data = bt.feeds.GenericCSVData(
            dataname=config.DATA_STOCKS_PATH + f'{ticker}.csv',
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
        cerebro.adddata(data, name=ticker)

    ## Add strategies to Cerebro
    cerebro.addstrategy(SMAStrategy, SMA_period=10)
    cerebro.addstrategy(SMAStrategy, SMA_period=30)
    cerebro.addstrategy(GoldenCrossStrategy, SMA_short_period=10, SMA_long_period=30)

    ## Set the position sizer
    cerebro.addsizer(StrategyPercentSizer, percents=10)

    ## Run Cerebro Engine
    strategies= cerebro.run()
    

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


    ## final reports
    # 1. transaction report
    all_trades = []
    for strat in strategies:
        # Extract the 'trade_history' list from each strategy
        all_trades.extend(strat.trade_history)
    
    # Create a DataFrame from the combined trade history to generate the report
    df_trades = pd.DataFrame(all_trades)
    
    if not df_trades.empty:
        # Sort by date
        df_trades.sort_values(by='date', inplace=True)
        
        # Save to CSV
        df_trades.to_csv(config.OUTPUT_REPORTS_PATH + 'transaction_report.csv', index=False)


    # 2. portfolio value report (variations)
    # take the value history of the first strategy (all share the same broker)
    portfolio_history = strategies[0].portfolio_values
    df_portfolio = pd.DataFrame(portfolio_history)
    df_portfolio.to_csv(config.OUTPUT_REPORTS_PATH + 'value_report_portfolio.csv', index=False)
    
    
    ## strategies resume
    strategy_transaction_resume.generate_strategy_transaction_resume()

    ## Plot the results
    cerebro.plot()

