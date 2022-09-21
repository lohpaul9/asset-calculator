from datetime import datetime
from currency_converter import CurrencyConverter
from ..baseentries.atdate import OwnedCashAtDate
from ..baseentries.single import OwnedCashEntry
from ..baseentries.transactions import StockTransaction
from unittest import TestCase
from ..histories.overall import OverallHistory

class TestAnalysisInst(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        transaction_list = [StockTransaction(datetime(2020, 5, 15).date(), 'D05.SI', 200, 10),
                            StockTransaction(datetime(2020, 6, 30).date(), 'D05.SI', 300, 20),
                            StockTransaction(datetime(2020, 7, 1).date(), 'D05.SI', 500, 16),
                            StockTransaction(datetime(2020, 8, 1).date(), 'D05.SI', 500, 10, 's'),
                            StockTransaction(datetime(2020, 4, 28).date(), 'BABA', 2, 100),
                            StockTransaction(datetime(2020, 5, 31).date(), 'BABA', 3, 200),
                            StockTransaction(datetime(2020, 6, 1).date(), 'BABA', 5, 100, 's'),
                            StockTransaction(datetime(2020, 7, 30).date(), 'BABA', 5, 100)]

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
        cls.stock_info = cls.overall_log.generate_stock_info()
        cls.cash_history_list = cash_history_list
        cls.transaction_list = transaction_list
        cls.converter = CurrencyConverter()

    def test_analysis_val_normal(self):
        analysis_inst = self.overall_log.generate_instant_analysis(datetime(2020, 6, 30).date(), 'SGD')
        act_st_val = analysis_inst.stock_value()
        act_cash_val = analysis_inst.cash_value()
        act_tot_val = act_cash_val + act_st_val

        expected_st_val = 500 * self.stock_info.price_at_date('D05.SI', datetime(2020, 6, 30).date())
        expected_cash_val = 5100 + self.converter.convert(1100, 'USD', 'SGD')
        expected_tot_val = expected_st_val + expected_cash_val
        self.assertAlmostEqual(expected_st_val, act_st_val, 5)
        self.assertAlmostEqual(expected_cash_val, act_cash_val, 5)
        self.assertAlmostEqual(expected_tot_val, act_tot_val, 5)

    def test_analysis_val_to_end(self):
        test_date = datetime(2022, 1, 1).date()
        analysis_inst = self.overall_log.generate_instant_analysis(test_date, 'SGD')
        act_st_val = analysis_inst.stock_value()
        act_cash_val = analysis_inst.cash_value()
        act_tot_val = act_cash_val + act_st_val

        expected_st_val = 500 * self.stock_info.price_at_date('D05.SI', test_date) + \
                        self.converter.convert(5 * self.stock_info.price_at_date('BABA', test_date), 'USD',
                                         'SGD')
        expected_cash_val = 5200 + self.converter.convert(1200, 'USD', 'SGD')
        expected_tot_val = expected_st_val + expected_cash_val
        self.assertAlmostEqual(expected_st_val, act_st_val, 5)
        self.assertAlmostEqual(expected_cash_val, act_cash_val, 5)
        self.assertAlmostEqual(expected_tot_val, act_tot_val, 5)

    def test_val_empty(self):
        test_date = datetime(2019, 7, 30).date()
        analysis_inst = self.overall_log.generate_instant_analysis(test_date, 'SGD')
        act_st_val = analysis_inst.stock_value()
        act_cash_val = analysis_inst.cash_value()
        act_tot_val = act_cash_val + act_st_val
        self.assertAlmostEqual(0, act_st_val, 5)
        self.assertAlmostEqual(0, act_cash_val, 5)
        self.assertAlmostEqual(0, act_tot_val, 5)
