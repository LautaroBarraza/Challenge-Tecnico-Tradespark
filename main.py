from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import pandas as pd

import src.config as config
import src.utils.data_loader as data_loader
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
            dataname=config.DATA_PATH + f'{ticker}.csv',
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


    cerebro.addstrategy(SMAStrategy, SMA_period=10)
    cerebro.addstrategy(SMAStrategy, SMA_period=30)
    cerebro.addstrategy(GoldenCrossStrategy, SMA_short_period=10, SMA_long_period=30)

    ## Set the position sizer
    cerebro.addsizer(StrategyPercentSizer, percents=10)

    ## Run Cerebro Engine
    strategies= cerebro.run()
    

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


    ## final reports
    # 1. REPORTE DE TRANSACCIONES
    all_trades = []
    for strat in strategies:
        # Extraemos la lista 'trade_history' de cada estrategia
        all_trades.extend(strat.trade_history)
    
    # Convertimos a DataFrame
    df_trades = pd.DataFrame(all_trades)
    
    if not df_trades.empty:
        # Ordenar por fecha
        df_trades.sort_values(by='date', inplace=True)
        
        # Guardar a CSV
        df_trades.to_csv('transaction_report.csv', index=False)


    # 2. REPORTE DE VALOR DE PORTFOLIO (Variaciones)
    # Tomamos la historia de valores de la primera estrategia (todas comparten el mismo broker)
    portfolio_history = strategies[0].portfolio_values
    df_portfolio = pd.DataFrame(portfolio_history)
    df_portfolio.to_csv('value_report_portfolio.csv', index=False)
    
    
    ## strategies resume
    


    cerebro.plot()

