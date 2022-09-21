import logging
from pprint import pformat
from .cash import OwnedCashHistory
from .stocks import StockTransactionHistory
from ..baseentries.atdate import *
from ..baseentries.transactions import StockTransaction
from ..assets.nwatdate import NwAtDate
from ..yfinscrape.allstockinfo import AllStockInfo
from ..analysis.instantaneous import AnalysisInstantaneous
from ..analysis.acrosstime import AnalysisAcrTime
from currency_converter import CurrencyConverter


class OverallHistory:
    def __init__(self, cash_at_date_entries: list[OwnedCashAtDate], stock_trxn_entries: list[StockTransaction],
                 stock_info: AllStockInfo = None):
        """
        Creates a overall history to be used as a facade for
        generating assets at date and for computing comparisons over time

        :param owned_cash_history: all owned cash history
        :param stock_trxn_history: all stock transaction entries
        """
        self.owned_cash_history = OwnedCashHistory(cash_at_date_entries)
        self.stock_trxn_history = StockTransactionHistory(stock_trxn_entries)
        self.stock_info = stock_info
        self.generate_stock_info()
        self.converter = CurrencyConverter()

    def generate_stock_info(self):
        if self.stock_info is None:
            ticker_list = self.stock_trxn_history.get_ticker_list()
            self.stock_info = AllStockInfo(ticker_list)
        return self.stock_info

    def generate_owned_stock_at_date(self, date):
        return self.stock_trxn_history.stock_owned_at_date(date)

    def generate_owned_cash_at_date(self, date):
        return self.owned_cash_history.cash_owned_at_date(date)

    def generate_stock_trxn_between_dates(self, date_bef, date_after):
        return self.stock_trxn_history.trxn_between_dates(date_bef, date_after)

    def generate_assets_at_date(self, date):
        """
        Creates a AssetsAtDate obj for EOD of given date
        :param date: datetime Obj
        :param curr: String curr
        :return:
        """
        if date > datetime.today().date():
            return ValueError
            logging.error('Cannot generate assets later than today')

        stocks_owned = self.generate_owned_stock_at_date(date)
        cash_owned = self.generate_owned_cash_at_date(date)

        # print(f"""-GENERATE NETWORTH OBJ ON EOD {date}--
        # STOCKS OWNED:
        # {pformat(stocks_owned)}
        # CASH OWNED: {pformat(cash_owned)}
        # INFO ON: {pformat(self.stock_info)}""")

        return NwAtDate(date, cash_owned, stocks_owned)

    def generate_instant_analysis(self, date, currency):
        nw = self.generate_assets_at_date(date)
        return AnalysisInstantaneous(self.stock_info, currency, self.converter, nw)

    def generate_analysis_across_time(self, date_bef: datetime, date_aft: datetime, currency: str):
        nw_bef = self.generate_assets_at_date(date_bef)
        nw_aft = self.generate_assets_at_date(date_aft)
        trxn_between = self.generate_stock_trxn_between_dates(date_bef, date_aft)
        return AnalysisAcrTime(self.stock_info, currency, self.converter, nw_bef, nw_aft, trxn_between)
