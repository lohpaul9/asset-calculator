from datetime import datetime
from currency_converter import CurrencyConverter
from ..baseentries.atdate import OwnedCashAtDate
from ..baseentries.single import OwnedCashEntry
from ..baseentries.transactions import StockTransaction
from unittest import TestCase
from ..histories.overall import OverallHistory

class TestAnalysisCross(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        transaction_list = [StockTransaction(datetime(2020, 4, 28).date(), 'BABA', 2, 100),
                            StockTransaction(datetime(2020, 5, 31).date(), 'BABA', 3, 200),
                            StockTransaction(datetime(2020, 6, 1).date(), 'BABA', 5, 100, 's'),
                            StockTransaction(datetime(2020, 6, 1).date(), 'BABA', 5, 160),
                            StockTransaction(datetime(2020, 7, 1).date(), 'BABA', 5, 300, 's'),
                            StockTransaction(datetime(2020, 7, 30).date(), 'BABA', 5, 100)]

        cash_dict1 = {}
        cash_dict1["USD"] = OwnedCashEntry('USD', 1000)
        cash_dict1["SGD"] = OwnedCashEntry('SGD', 5000)
        oc1 = OwnedCashAtDate(datetime(2020, 1, 1).date(), cash_dict1)

        cash_dict2 = {}
        cash_dict2["USD"] = OwnedCashEntry('USD', 1100)
        cash_dict2["SGD"] = OwnedCashEntry('SGD', 5100)
        oc2 = OwnedCashAtDate(datetime(2020, 5, 31).date(), cash_dict2)

        cash_dict3 = {}
        cash_dict3["USD"] = OwnedCashEntry('USD', 1200)
        cash_dict3["SGD"] = OwnedCashEntry('SGD', 5200)
        oc3 = OwnedCashAtDate(datetime(2020, 6, 1).date(), cash_dict3)

        cash_history_list = [oc1, oc2, oc3]

        cls.overall_log = OverallHistory(cash_history_list, transaction_list)
        cls.stock_info = cls.overall_log.generate_stock_info()
        cls.cash_history_list = cash_history_list
        cls.transaction_list = transaction_list
        cls.converter = CurrencyConverter()

    def test_raw_total_growth_normal(self):
        analysis = self.overall_log.generate_analysis_across_time(datetime(2020, 4, 28).date(),
                                                                  datetime(2020, 7, 30).date(), 'SGD')

        exp_nw_bef = 2 * self.stock_info.price_at_date('BABA', datetime(2020, 4, 28).date())
        conv_nw_bef = self.converter.convert(exp_nw_bef + 1000, 'USD', 'SGD') + 5000

        exp_nw_aft = 5 * self.stock_info.price_at_date('BABA', datetime(2020, 7, 30).date())
        conv_nw_aft = self.converter.convert(exp_nw_aft + 1200, 'USD', 'SGD') + 5200

        self.assertAlmostEqual(conv_nw_aft - conv_nw_bef, analysis.raw_total_growth(), 5)

    def test_raw_total_growth_from_scratch(self):
        analysis = self.overall_log.generate_analysis_across_time(datetime(2018, 1, 1).date(),
                                                                  datetime(2020, 7, 30).date(), 'SGD')
        conv_nw_bef = 0
        exp_nw_aft = 5 * self.stock_info.price_at_date('BABA', datetime(2020, 7, 30).date())
        conv_nw_aft = self.converter.convert(exp_nw_aft + 1200, 'USD', 'SGD') + 5200

        self.assertAlmostEqual(conv_nw_aft - conv_nw_bef, analysis.raw_total_growth(), 5)

    def test_percent_total_growth(self):
        date_bef = datetime(2020, 5, 31).date()
        date_aft = datetime(2020, 6, 1).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        exp_nw_bef = 5 * self.stock_info.price_at_date('BABA', date_bef)
        conv_nw_bef = self.converter.convert(exp_nw_bef + 1100, 'USD', 'SGD') + 5100

        exp_nw_aft = 5 * self.stock_info.price_at_date('BABA', date_aft)
        conv_nw_aft = self.converter.convert(exp_nw_aft + 1200, 'USD', 'SGD') + 5200

        exp_percent_growth = (conv_nw_aft - conv_nw_bef) *100 / conv_nw_bef

        self.assertAlmostEqual(exp_percent_growth, analysis.percent_total_growth(), 5)

    def test_percent_total_growth_from_scratch(self):
        analysis = self.overall_log.generate_analysis_across_time(datetime(2018, 1, 1).date(),
                                                                  datetime(2020, 7, 30).date(),'SGD')

        self.assertEqual(None, analysis.percent_total_growth())

    def test_raw_portfolio_growth(self):
        date_bef = datetime(2020, 5, 31).date()
        date_aft = datetime(2020, 6, 1).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        exp_nw_bef = 5 * self.stock_info.price_at_date('BABA', date_bef)
        conv_nw_bef = self.converter.convert(exp_nw_bef, 'USD', 'SGD')

        exp_nw_aft = 5 * self.stock_info.price_at_date('BABA', date_aft)
        conv_nw_aft = self.converter.convert(exp_nw_aft, 'USD', 'SGD')

        exp_portfolio_growth = conv_nw_aft - conv_nw_bef

        self.assertAlmostEqual(exp_portfolio_growth, analysis.raw_portfolio_growth(), 5)

    def test_total_closed_all(self):
        date_bef = datetime(2020, 1, 1).date()
        date_aft = datetime(2021, 1, 1).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        total_closed = self.converter.convert(400, 'USD', 'SGD')

        self.assertAlmostEqual(total_closed, analysis.total_closed(), 5)

    def test_total_closed_single(self):
        date_bef = datetime(2020, 6, 1).date()
        date_aft = datetime(2020, 8, 1).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        total_closed = self.converter.convert(700, 'USD', 'SGD')

        self.assertAlmostEqual(total_closed, analysis.total_closed(), 5)

    def test_total_closed_zero(self):
        date_bef = datetime(2020, 4, 1).date()
        date_aft = datetime(2020, 5, 31).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        self.assertAlmostEqual(0, analysis.total_closed(), 5)

    def test_total_closed_no_trxn(self):
        date_bef = datetime(2020, 1, 1).date()
        date_aft = datetime(2020, 1, 2).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        self.assertAlmostEqual(0, analysis.total_closed(), 5)

    def test_total_profit_normal(self):
        date_bef = datetime(2020, 5, 31).date()
        date_aft = datetime(2020, 7, 1).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        exp_prof_bef = 5 * (self.stock_info.price_at_date('BABA', date_bef) - 160)
        conv_prof_bef = self.converter.convert(exp_prof_bef, 'USD', 'SGD')

        exp_prof_aft = 0
        conv_prof_aft = self.converter.convert(exp_prof_aft, 'USD', 'SGD')

        conv_closed = self.converter.convert(400, 'USD', 'SGD')

        exp_total_profit = conv_prof_aft - conv_prof_bef + conv_closed

        self.assertAlmostEqual(exp_total_profit, analysis.raw_profit_loss(), 5)

    def test_total_profit_from_scratch(self):
        date_bef = datetime(2020, 1, 1).date()
        date_aft = datetime(2020, 6, 1).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        exp_prof_bef = 0
        conv_prof_bef = self.converter.convert(exp_prof_bef, 'USD', 'SGD')

        exp_prof_aft = 5 * (self.stock_info.price_at_date('BABA', date_aft) - 160)
        conv_prof_aft = self.converter.convert(exp_prof_aft, 'USD', 'SGD')

        conv_closed = self.converter.convert(-300, 'USD', 'SGD')

        exp_total_profit = conv_prof_aft - conv_prof_bef + conv_closed

        self.assertAlmostEqual(exp_total_profit, analysis.raw_profit_loss(), 5)

    def test_total_profit_throughout(self):
        date_bef = datetime(2020, 1, 1).date()
        date_aft = datetime(2021, 1, 1).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        exp_prof_bef = 0
        conv_prof_bef = self.converter.convert(exp_prof_bef, 'USD', 'SGD')

        exp_prof_aft = 5 * (self.stock_info.price_at_date('BABA', date_aft) - 100)
        conv_prof_aft = self.converter.convert(exp_prof_aft, 'USD', 'SGD')

        conv_closed = self.converter.convert(400, 'USD', 'SGD')

        exp_total_profit = conv_prof_aft - conv_prof_bef + conv_closed

        self.assertAlmostEqual(exp_total_profit, analysis.raw_profit_loss(), 5)

    def test_total_profit_between(self):
        date_bef = datetime(2020, 5, 31).date()
        date_aft = datetime(2020, 7, 30).date()
        analysis = self.overall_log.generate_analysis_across_time(date_bef, date_aft,
                                                                  'SGD')

        exp_prof_bef = 5 * (self.stock_info.price_at_date('BABA', date_bef) - 160)
        conv_prof_bef = self.converter.convert(exp_prof_bef, 'USD', 'SGD')

        exp_prof_aft = 5 * (self.stock_info.price_at_date('BABA', date_aft) - 100)
        conv_prof_aft = self.converter.convert(exp_prof_aft, 'USD', 'SGD')

        conv_closed = self.converter.convert(400, 'USD', 'SGD')

        exp_total_profit = conv_prof_aft - conv_prof_bef + conv_closed

        self.assertAlmostEqual(exp_total_profit, analysis.raw_profit_loss(), 5)


