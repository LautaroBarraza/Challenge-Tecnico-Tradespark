import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


import src.config as config


def generate_strategy_transaction_resume():
    """
    Generate a summary report and visualizations for strategy transactions.
    This function reads transaction data from a CSV file, computes summary statistics
    for each strategy, and generates visualizations to analyze strategy performance.
    """


    data_transactions = pd.read_csv(config.OUTPUT_REPORTS_PATH + 'transaction_report.csv')


    data_transactions= data_transactions[data_transactions['operation']=='TRADE_CLOSE']
    strategies=data_transactions['strategy'].unique()
    columns = ['strategy', 'total_trades', 'profitable_trades', 'losing_trades', 'win_rate_pct', 'total_profit', 'avg_profit', 'max_profit', 'max_loss']
    resume_list = []
    resume_strat = pd.DataFrame()
    for strat in strategies:
        data_strat = data_transactions[data_transactions['strategy'] == strat]
        
        total_trades = len(data_strat)
        
        
        if total_trades > 0:
            profitable_trades = len(data_strat[data_strat['profit_net'] > 0])
            losing_trades = len(data_strat[data_strat['profit_net'] <= 0])
            
            win_rate = (profitable_trades / total_trades) * 100
            
            total_profit = data_strat['profit_net'].sum()
            avg_profit = data_strat['profit_net'].mean()
            max_profit = data_strat['profit_net'].max()
            max_loss = data_strat['profit_net'].min()
            
            resume_list.append({
                'strategy': strat,
                'total_trades': total_trades,
                'profitable_trades': profitable_trades,
                'losing_trades': losing_trades,
                'win_rate_pct': round(win_rate, 2), 
                'total_profit': total_profit,
                'avg_profit': avg_profit,
                'max_profit': max_profit,
                'max_loss': max_loss
            })
    resume_strat = pd.DataFrame(resume_list, columns=columns)
    resume_strat.to_csv(config.OUTPUT_ANALYSIS_PATH + 'strategies_resume.csv', index=False)


    ## Data Visualization
    ## Total Profit.

    plt.figure(figsize=(12, 6))
    data_transactions.boxplot(column='profit_net', by='strategy', grid=False)
    plt.title('Profit Distribution by Strategy')
    plt.suptitle('')
    plt.xlabel('Strategy')
    plt.ylabel('Profit Net')
    plt.xticks(rotation=90)
    plt.savefig(config.OUTPUT_ANALYSIS_FIGURES_PATH + 'strategies_profit_distribution.png')
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.bar(resume_strat['strategy'], resume_strat['total_profit'])
    plt.xlabel('Strategy')
    plt.xticks(rotation=90)
    plt.ylabel('Total Profit')
    plt.title('Total Profit by Strategy')
    plt.savefig(config.OUTPUT_ANALYSIS_FIGURES_PATH + 'strategies_total_profit.png')
    plt.close()



    ## Trades
    strats = resume_strat['strategy'].tolist()
    trades = {
        'profitable_trades': resume_strat['profitable_trades'].tolist(),
        'losing_trades': resume_strat['losing_trades'].tolist()
    }

    x = np.arange(len(strats))

    width = 0.6  # the width of the bars: can also be len(x) sequence


    fig, ax = plt.subplots()
    bottom = np.zeros(3)

    for trade, exitos  in trades.items():
        p = ax.bar(strats, exitos, width, label=trade, bottom=bottom)
        bottom += exitos

        ax.bar_label(p, label_type='center')

    ax.set_title('Number of trades by type and strategy')
    ax.legend()

    plt.savefig(config.OUTPUT_ANALYSIS_FIGURES_PATH + 'strategies_trades_summary.png')
    plt.close()