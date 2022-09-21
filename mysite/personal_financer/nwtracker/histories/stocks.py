import logging
from datetime import timedelta

from .timesorted import SortedByDate
from ..baseentries.transactions import *
from ..baseentries.single import *
from ..baseentries.atdate import *

class StockTransactionHistory(SortedByDate):

    def trxn_time_comparator(entry: StockTransaction):
        converted_datetime = datetime(entry.date.year, entry.date.month, entry.date.day)
        if entry.type == 's':
            return converted_datetime + timedelta(seconds=10)
        else:
            return converted_datetime

    def __init__(self, transaction_entries: list[StockTransaction]):
        self.sorted = transaction_entries
        self.sorted.sort(key=StockTransactionHistory.trxn_time_comparator)

    # To-Do : Refine Error handling for this error
    def stock_owned_at_date(self, date: datetime) -> OwnedStockAtDate:
        """
        return stocks owned by date EOD generated from a list of transactions
        :param date: datetime obj
        :return: OwnedStockAtDate obj
        """
        entries_before = self.entries_by_date(date)
        stocks = {}
        for trxn_entry in entries_before:
            if trxn_entry.ticker not in stocks:
                if trxn_entry.type == 's':
                    logging.error(
                        f"Stock sell entry registered before any were found in portfolio for {trxn_entry.ticker}")
                    raise ValueError
                else:
                    stocks[trxn_entry.ticker] = OwnedStockEntry(trxn_entry.ticker,
                                                                trxn_entry.quantity, trxn_entry.price)
            else:
                stocks[trxn_entry.ticker].handle_transaction(trxn_entry)
        stocks_at_date = OwnedStockAtDate(date, stocks)
        return stocks_at_date

    def trxn_between_dates(self, date_bef: datetime, date_after: datetime) -> list[StockTransaction]:
        """
        returns all stock transaction entries between earlier date EOD (ie next day)
        and later date EOD

        :param date_bef:  earlier date
        :param DateLater:  later date
        :return stock transactions in given period
        """
        return self.entries_between_dates(date_bef, date_after)

    def get_ticker_list(self):
        ticker_list = []
        for transaction in self.sorted:
            if transaction.ticker not in ticker_list:
                ticker_list.append(transaction.ticker)
        return ticker_list

