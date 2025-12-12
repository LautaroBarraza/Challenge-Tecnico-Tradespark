import backtrader as bt

class BaseStrategy(bt.Strategy):

    """
    Base Strategy Class
    This class serves as a base for all trading strategies, providing common functionality
    such as order management, trade logging, and portfolio tracking.
    """


    def __init__(self):

        # Pending orders per data
        self.orders = {d: None for d in self.datas}

        # Trade history
        self.trade_history = []

        # Portfolio values
        self.portfolio_values = []

        # open lots of the strategy
        self.ledger = {d: [] for d in self.datas}

        # unique strategy name with params
        params_str = ""
        self.strat_name = self.__class__.__name__
        try:
            for name, value in self.params._getitems():
                actual_value = getattr(self.params, name)
                params_str += f"{actual_value}"
            self.strat_name += params_str
        except:
            pass


    def next(self):
        if len(self.datas) > 0:
            dt = self.datas[0].datetime.date(0)
            self.portfolio_values.append(
                {
                    "date": dt,
                    "total_value": self.broker.getvalue(),
                    "diary_variation": self.broker.getvalue() - self.broker.startingcash,
                    "cash": self.broker.getcash(),
                })


    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt} , {txt}")


    def notify_order(self, order):
        data = order.data
        stockname = getattr(data, "_name", str(data))

        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status == order.Completed:

            # register buy
            if order.isbuy():
                self.log(f"BUY EXECUTED {stockname}, price {order.executed.price}, size {order.executed.size}")

                size = int(order.executed.size)
                if size > 0:
                    self.ledger[data].append({
                        'size': size,
                        'remaining': size,
                        'price': order.executed.price,
                        'opened_dt': self.datas[0].datetime.date(0)
                    })

            # register sell
            else:
                self.log(f"SELL EXECUTED {stockname}, price {order.executed.price}, size {order.executed.size}")

                size = int(abs(order.executed.size))
                remaining = size
                lots = self.ledger[data]
                new_lots = []

                for lot in lots:

                    if remaining <= 0:
                        new_lots.append(lot)
                        continue

                    if lot['remaining'] <= remaining:
                        remaining -= lot['remaining']
                        lot['remaining'] = 0
                    else:
                        lot['remaining'] -= remaining
                        remaining = 0
                        new_lots.append(lot)

                self.ledger[data] = [l for l in new_lots if l['remaining'] > 0]

            # save trade history
            self.trade_history.append({
                "date": self.datas[0].datetime.date(0),
                "stock": stockname,
                "strategy": self.strat_name,
                "operation": "BUY" if order.isbuy() else "SELL",
                "price": order.executed.price,
                "size": order.executed.size,
                "capital": self.broker.getvalue(),
                
            })

        self.orders[data] = None


    def notify_trade(self, trade):
        if trade.isclosed:
            data= trade.data

            stock=getattr(data, "_name", str(data))
            self.log(f"CLOSED TRADE {stock}, GROSS PNL {trade.pnl}, NET PNL {trade.pnlcomm}")
            self.trade_history.append({
                "date": self.datas[0].datetime.date(0),
                "stock": stock,
                "strategy": self.strat_name,
                "operation": "TRADE_CLOSE",
                "price": None,
                "size": trade.size,
                "profit_gross": trade.pnl,
                "profit_net": trade.pnlcomm,
                "capital": self.broker.getvalue()
        })

    def position(self, data):
        """Get the current position size for a given data feed.
        :param data: The data feed (stock).
        :return: Current position size.
        """
        return sum(lot['remaining'] for lot in self.ledger[data])
