from ..baseentries.atdate import OwnedCashAtDate, OwnedStockAtDate, Dated
import copy
from ..baseentries.single import OwnedStockEntry, OwnedCashEntry

class NwAtDate(Dated):

    def __init__(self, date, owned_cash: OwnedCashAtDate, owned_stocks: OwnedStockAtDate):
        """
        Represents all owned assets at a given date

        :param date: datetimeObj
        :param owned_cash: all cash owned at date of diff curr
        :param owned_stocks: all stocks owned at date
        """
        self.date = date
        self.cash = owned_cash
        self.stocks = owned_stocks

        # To be implemented
        self.liabilities = None

    def all_stocks(self) -> dict[str, OwnedStockEntry]:
        return copy.deepcopy(self.stocks.entries)

    def all_cash(self) -> dict[str, OwnedCashEntry]:
        return copy.deepcopy(self.cash.entries)

    def __repr__(self):
        return f"NETWORTH obj generated for before {self.date}"
