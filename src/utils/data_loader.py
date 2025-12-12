import yfinance as yf
import pandas as pd
import os
import src.config as config


def load_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Load historical stock data from Yahoo Finance and save it to a CSV file.

    :param ticker: Stock ticker symbol.
    :param start_date: Start date for the data in 'YYYY-MM-DD' format.
    :param end_date: End date for the data in 'YYYY-MM-DD' format.
    :return: DataFrame containing historical stock dataor none if data is not available.
    """
    
    data = yf.download(ticker, start=start_date, end=end_date)
    
    stock_name = f'{ticker}.csv'
    
    # 1. Check if is multiindex and flatten it
    if isinstance(data.columns, pd.MultiIndex):
        # Keep only level 0 (Close, Open, etc) and discard the level 'AAPL'
        data.columns = data.columns.get_level_values(0)
    
    # 2. Ensure no empty rows at the beginning
    data = data.dropna()
    
    data.to_csv(os.path.join(config.DATA_STOCKS_PATH, stock_name))
    
    if data.empty:
        return None

    return stock_name

