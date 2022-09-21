from unittest import TestCase
from ..histories.stocks import *
from ..histories.cash import *
from ..baseentries.atdate import *

from datetime import datetime


class TestHistory(TestCase):

    def setUp(self):
        transaction_list = [StockTransaction(datetime(2020, 5, 15).date(), 'D05.SI', 200, 10),
                            StockTransaction(datetime(2020, 6, 30).date(), 'D05.SI', 300, 20),
                            StockTransaction(datetime(2020, 7, 1).date(), 'D05.SI', 500, 16),
                            StockTransaction(datetime(2020, 8, 1).date(), 'D05.SI', 500, 10, 's'),
                            StockTransaction(datetime(2020, 4, 28).date(), 'BABA', 2, 100),
                            StockTransaction(datetime(2020, 5, 31).date(), 'BABA', 3, 200),
                            StockTransaction(datetime(2020, 6, 1).date(), 'BABA', 5, 100, 's'),
                            StockTransaction(datetime(2020, 7, 30).date(), 'BABA', 5, 100)]

        self.transaction_list = transaction_list
        # self.trxn_history = StockTransactionHistory(transaction_list)

        cash_dict1 = {}
        cash_dict1["USD"] = OwnedCashEntry('USD', 1000)
        cash_dict1["SGD"] = OwnedCashEntry('SGD', 5000)
        oc1 = OwnedCashAtDate(datetime(2020, 1, 1).date(), cash_dict1)

        cash_dict2 = {}
        cash_dict2["USD"] = OwnedCashEntry('USD', 1100)
        cash_dict2["SGD"] = OwnedCashEntry('SGD', 5100)
        oc2 = OwnedCashAtDate(datetime(2020, 6, 30).date(), cash_dict2)

        cash_dict2 = {}
        cash_dict2["USD"] = OwnedCashEntry('USD', 1100)
        cash_dict2["SGD"] = OwnedCashEntry('SGD', 5100)
        oc3 = OwnedCashAtDate(datetime(2020, 6, 30).date(), cash_dict2)

        cash_dict3 = {}
        cash_dict3["USD"] = OwnedCashEntry('USD', 1200)
        cash_dict3["SGD"] = OwnedCashEntry('SGD', 5200)
        oc3 = OwnedCashAtDate(datetime(2020, 7, 1).date(), cash_dict3)

        cash_history_list = [oc1, oc2, oc3]
        self.cash_history_list = cash_history_list

class TestStockTransactionHistory(TestHistory):

    def test_is_sorted(self):
        test_trxn_history = StockTransactionHistory(self.transaction_list.copy())
        all_trxn_list = test_trxn_history.entries_by_date(datetime.today().date())
        for i in range(len(all_trxn_list) - 1):
            self.assertTrue(all_trxn_list[i].rounded_date() <= all_trxn_list[i + 1].rounded_date())
            self.assertTrue(all_trxn_list[i] in self.transaction_list)

    def test_sorted_buy_before_sells(self):
        transaction_list = [StockTransaction(datetime(2020, 7, 1).date(), 'D05.SI', 500, 1, 's'),
                            StockTransaction(datetime(2020, 7, 1).date(), 'D05.SI', 500, 2),
                            StockTransaction(datetime(2020, 7, 1).date(), 'D05.SI', 500, 3, 's')]
        history = StockTransactionHistory(transaction_list)
        sorted_trxn_list = history.entries_by_date(datetime.today().date())
        print(sorted_trxn_list)
        self.assertTrue(sorted_trxn_list[0].type == 'b')
        self.assertTrue(sorted_trxn_list[1].type == 's')
        self.assertTrue(sorted_trxn_list[2].type == 's')


    def test_empty(self):
        test_trxn_history = StockTransactionHistory([])
        all_trxn_list = test_trxn_history.entries_by_date(datetime.today().date())
        self.assertTrue(len(all_trxn_list) == 0)

    def test_entries_by_date_normal(self):
        test_trxn_history = StockTransactionHistory(self.transaction_list.copy())
        entries_before = test_trxn_history.entries_by_date(datetime(2020, 6, 30).date())
        for entry in entries_before:
            self.assertTrue(entry in self.transaction_list)
        self.assertEqual(len(entries_before), 5)
        self.assertTrue(self.transaction_list[2] not in entries_before)
        self.assertTrue(self.transaction_list[3] not in entries_before)
        self.assertTrue(self.transaction_list[7] not in entries_before)

    def test_stocks_owned_by_date_EOD_inclusive(self):
        test_trxn_history = StockTransactionHistory(self.transaction_list.copy())
        stock_by_date = test_trxn_history.stock_owned_at_date(datetime(2020, 6, 30).date())
        stock_entries = stock_by_date.entries
        self.assertEqual(stock_entries['BABA'].quantity, 0)
        self.assertEqual(stock_entries['BABA'].price, 160)
        self.assertEqual(stock_entries['D05.SI'].quantity, 500)
        self.assertEqual(stock_entries['D05.SI'].price, 16)

    def test_stocks_By_Date_Today(self):
        test_trxn_history = StockTransactionHistory(self.transaction_list.copy())
        stock_by_date = test_trxn_history.stock_owned_at_date(datetime.today().date())
        stock_entries = stock_by_date.entries
        self.assertEqual(stock_entries['BABA'].quantity, 5)
        self.assertEqual(stock_entries['BABA'].price, 100)
        self.assertEqual(stock_entries['D05.SI'].quantity, 500)
        self.assertEqual(stock_entries['D05.SI'].price, 16)


    def test_stocks_By_Date_Single_Transact(self):
        test_trxn_history = StockTransactionHistory(self.transaction_list.copy())
        stock_by_date = test_trxn_history.stock_owned_at_date(datetime(2020, 4, 28).date())
        stock_entries = stock_by_date.entries
        self.assertEqual(stock_entries['BABA'].quantity, 2)
        self.assertEqual(stock_entries['BABA'].price, 100)
        self.assertEqual(1, len(stock_entries))


    def test_stocks_By_Date_Empty(self):
        test_trxn_history = StockTransactionHistory(self.transaction_list.copy())
        stock_by_date = test_trxn_history.stock_owned_at_date(datetime(2020, 1, 1).date())
        stock_entries = stock_by_date.entries
        self.assertEqual(0, len(stock_entries))

    def test_ticker_list(self):
        test_trxn_history = StockTransactionHistory(self.transaction_list.copy())
        ticker_list = test_trxn_history.get_ticker_list()
        self.assertTrue('BABA' in ticker_list)
        self.assertTrue('D05.SI' in ticker_list)
        self.assertEqual(2, len(ticker_list))

class TestOwnedCashHistory(TestHistory):

    def test_is_sorted(self):
        test_cash_history = OwnedCashHistory(self.cash_history_list.copy())
        all_entries = test_cash_history.entries_by_date(datetime(2022, 10, 10).date())
        for i in range(len(all_entries) - 1):
            self.assertTrue(all_entries[i].rounded_date() <= all_entries[i + 1].rounded_date())
            self.assertTrue(all_entries[i] in self.cash_history_list)

    def test_empty(self):
        test_cash_history = OwnedCashHistory([])
        all_entries = test_cash_history.entries_by_date(datetime(2022, 10, 10).date())
        self.assertEqual(0, len(all_entries))

    def test_by_date(self):
        test_cash_history = OwnedCashHistory(self.cash_history_list.copy())
        all_entries = test_cash_history.entries_by_date(datetime(2020, 6, 30).date())
        self.assertEqual(2, len(all_entries))
        self.assertTrue(self.cash_history_list[0] in all_entries)
        self.assertTrue(self.cash_history_list[1] in all_entries)

    def test_by_date_empty(self):
        test_cash_history = OwnedCashHistory(self.cash_history_list.copy())
        all_entries = test_cash_history.entries_by_date(datetime(2019, 6, 30).date())
        self.assertEqual(0, len(all_entries))

    def test_owned_by_date(self):
        test_cash_history = OwnedCashHistory(self.cash_history_list.copy())
        test_cash_owned = test_cash_history.cash_owned_at_date(datetime(2020, 6, 30).date()).get_assets()
        self.assertEqual(2, len(test_cash_owned))
        self.assertEqual(5100, test_cash_owned['SGD'].quantity)
        self.assertEqual(1100, test_cash_owned['USD'].quantity)

    def test_owned_by_date_eod(self):
        test_cash_history = OwnedCashHistory(self.cash_history_list.copy())
        test_cash_owned_entries = test_cash_history.cash_owned_at_date(datetime(2020, 7, 1).date()).get_assets()
        self.assertEqual(2, len(test_cash_owned_entries))
        self.assertEqual(5200, test_cash_owned_entries['SGD'].quantity)
        self.assertEqual(1200, test_cash_owned_entries['USD'].quantity)

    def test_owned_before_date_empty(self):
        test_cash_history = OwnedCashHistory(self.cash_history_list.copy())
        test_cash_owned_entries = test_cash_history.cash_owned_at_date(datetime(2018, 7, 1).date()).get_assets()
        self.assertEqual(0, len(test_cash_owned_entries))

