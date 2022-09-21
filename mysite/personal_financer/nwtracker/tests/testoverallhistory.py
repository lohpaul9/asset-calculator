from datetime import datetime

from ..baseentries.atdate import OwnedCashAtDate
from ..baseentries.single import OwnedCashEntry
from ..baseentries.transactions import StockTransaction
from unittest import TestCase
from ..histories.overall import OverallHistory

class TestOverallHistory(TestCase):

        @classmethod
        def setUpClass(cls) -> None:
            transaction_list = []
            transaction_list.append(StockTransaction(datetime(2020, 5, 15).date(), 'D05.SI', 200, 10))
            transaction_list.append(StockTransaction(datetime(2020, 6, 30).date(), 'D05.SI', 300, 20))
            transaction_list.append(StockTransaction(datetime(2020, 7, 1).date(), 'D05.SI', 500, 16))
            transaction_list.append(StockTransaction(datetime(2020, 8, 1).date(), 'D05.SI', 500, 10, 's'))

            transaction_list.append(StockTransaction(datetime(2020, 4, 28).date(), 'BABA', 2, 100))
            transaction_list.append(StockTransaction(datetime(2020, 5, 31).date(), 'BABA', 3, 200))
            transaction_list.append(StockTransaction(datetime(2020, 6, 1).date(), 'BABA', 5, 100, 's'))
            transaction_list.append(StockTransaction(datetime(2020, 7, 30).date(), 'BABA', 5, 100))

            cash_dict1 = {}
            cash_dict1["USD"] = OwnedCashEntry('USD', 1000)
            cash_dict1["SGD"] = OwnedCashEntry('SGD', 5000)
            oc1 = OwnedCashAtDate(datetime(2020, 1, 1).date(), cash_dict1)

            cash_dict2 = {}
            cash_dict2["USD"] = OwnedCashEntry('USD', 1100)
            cash_dict2["SGD"] = OwnedCashEntry('SGD', 5100)
            oc2 = OwnedCashAtDate(datetime(2020, 6, 30).date(), cash_dict2)

            cash_dict3 = {}
            cash_dict3["USD"] = OwnedCashEntry('USD', 1200)
            cash_dict3["SGD"] = OwnedCashEntry('SGD', 5200)
            oc3 = OwnedCashAtDate(datetime(2020, 7, 1).date(), cash_dict3)

            cash_history_list = [oc1, oc2, oc3]

            cls.overall_log = OverallHistory(cash_history_list, transaction_list)
            cls.cash_history_list = cash_history_list
            cls.transaction_list = transaction_list

        def test_generate_nw_normal(self):
            nw = self.overall_log.generate_assets_at_date(datetime(2020, 7, 1).date())
            self.assertEqual(0, nw.all_stocks()['BABA'].quantity)
            self.assertEqual(160, nw.all_stocks()['BABA'].price)
            self.assertEqual(1000, nw.all_stocks()['D05.SI'].quantity)
            self.assertEqual(16, nw.all_stocks()['D05.SI'].price)
            self.assertEqual(2, len(nw.all_stocks()))

            self.assertEqual(5200, nw.all_cash()['SGD'].quantity)
            self.assertEqual(1200, nw.all_cash()['USD'].quantity)
            self.assertEqual(2, len(nw.all_cash()))

        def test_generate_nw_all(self):
            nw = self.overall_log.generate_assets_at_date(datetime(2021, 7, 1).date())
            self.assertEqual(5, nw.all_stocks()['BABA'].quantity)
            self.assertEqual(100, nw.all_stocks()['BABA'].price)
            self.assertEqual(500, nw.all_stocks()['D05.SI'].quantity)
            self.assertEqual(16, nw.all_stocks()['D05.SI'].price)
            self.assertEqual(2, len(nw.all_stocks()))

            self.assertEqual(5200, nw.all_cash()['SGD'].quantity)
            self.assertEqual(1200, nw.all_cash()['USD'].quantity)
            self.assertEqual(2, len(nw.all_cash()))

        def test_generate_date_before_first(self):
            nw = self.overall_log.generate_assets_at_date(datetime(2018, 7, 1).date())
            self.assertEqual(0, len(nw.all_stocks()))
            self.assertEqual(0, len(nw.all_cash()))

        def test_trxn_between_dates_all(self):
            date_bef = datetime(2020, 4, 27).date()
            date_after = datetime(2020, 8, 2).date()
            trxn_between = self.overall_log.generate_stock_trxn_between_dates(date_bef, date_after)
            self.assertEqual(8, len(trxn_between))

        def test_trxn_between_dates_eod_invariant(self):
            date_bef = datetime(2020, 4, 28).date()
            date_after = datetime(2020, 7, 30).date()
            trxn_between = self.overall_log.generate_stock_trxn_between_dates(date_bef, date_after)
            self.assertEqual(6, len(trxn_between))
            print(trxn_between)
            for trxn in trxn_between:
                self.assertTrue(date_bef < trxn.rounded_date() <= date_after)

        def gen_nw_error(self):
            self.assertRaises(ValueError, lambda : self.overall_log.generate_assets_at_date(datetime(2050, 1,1).date()))