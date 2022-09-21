import logging
import pprint
from .instantaneous import AnalysisInstantaneous
from ..yfinscrape.allstockinfo import AllStockInfo
from ..assets.nwatdate import NwAtDate
from currency_converter import CurrencyConverter
from ..baseentries.transactions import StockTransaction
from ..baseentries.single import OwnedStockEntry

class AnalysisAcrTime:
    def __init__(self, stock_info: AllStockInfo, currency: str, converter: CurrencyConverter,
                 nw_before: NwAtDate, nw_after: NwAtDate, trxn_between: list[StockTransaction]):
        self.stock_info = stock_info
        self.currency = currency
        self.converter = converter
        self.nw_before = nw_before
        self.nw_after = nw_after
        self.date_before = nw_before.rounded_date()
        self.date_after = nw_after.rounded_date()
        self.analysis_before = AnalysisInstantaneous(stock_info, currency, converter, nw_before)
        self.analysis_after = AnalysisInstantaneous(stock_info, currency, converter, nw_after)
        self.trxn_between = trxn_between

    def raw_total_growth(self):
        return self.analysis_after.total_value() - self.analysis_before.total_value()

    def percent_total_growth(self):
        try:
            return 100 * self.raw_total_growth() / self.analysis_before.total_value()
        except ZeroDivisionError:
            return None

    def raw_portfolio_growth(self):
        return self.analysis_after.stock_value() - self.analysis_before.stock_value()

    def total_closed(self):
        total_closed = 0
        # print(f"--CALCULATING TOTAL CLOSED PROFIT BETWENN {self.date_before} {self.date_after}--")
        rolling_portfolio = self.nw_before.all_stocks()
        # print(rolling_portfolio)
        for trxn in self.trxn_between:
            stock_held = rolling_portfolio.get(trxn.ticker, None)
            if stock_held == None and trxn.type == 'b':
                rolling_portfolio[trxn.ticker] = OwnedStockEntry(trxn.ticker, trxn.quantity, trxn.price)
            elif stock_held == None and trxn.type == 's':
                logging.error("Cannot sell stock of zero quantity")
                raise ValueError
            else:
                stock_held.handle_transaction(trxn)
                if trxn.type == 's':
                    closed_delta = (trxn.price - stock_held.price) * trxn.quantity
                    converted_delta = self.converter.convert(closed_delta,
                                                             self.stock_info.local_curr(trxn.ticker), self.currency)
                    total_closed += converted_delta

                    # print(f'''{trxn.ticker} {trxn.date}
                    #                         SELlPRICE:{trxn.price}
                    #                         AVGHOLDINGPRICE:{stock_held.price}
                    #                         PROFIT/SHARE:{closed_delta / trxn.quantity}
                    #                         TOTAL PROFIT:{closed_delta} {self.stock_info.local_curr(trxn.ticker)} -> {converted_delta} {self.currency}
                    #                         ROLLINGCLOSEDPROFIT: {total_closed}''')
        # print(f"TOTAL CLOSED: {total_closed}{self.currency}\n")
        return total_closed

    def raw_profit_loss(self):
        profit_bef = self.analysis_before.stock_value() - self.analysis_before.stocks_bought_value()
        profit_aft = self.analysis_after.stock_value() - self.analysis_after.stocks_bought_value()
        total_closed = self.total_closed()
        return profit_aft + total_closed - profit_bef

    def raw_non_mkt_growth(self):
        return self.raw_total_growth() - self.raw_profit_loss()

    def all_statistics(self):
        cmpr_info = {}
        cmpr_info["raw_total_growth"] = self.raw_total_growth()
        cmpr_info["percent_total_growth"] = self.percent_total_growth()
        cmpr_info["raw_portfolio_growth"] = self.raw_portfolio_growth()
        cmpr_info["raw_profit_and_loss"] = self.raw_profit_loss()
        cmpr_info["raw_non_market_growth"] = self.raw_non_mkt_growth()
        return cmpr_info


