from unittest import TestCase
from datetime import datetime
from ..yfinscrape.allstockinfo import AllStockInfo

class TestAllStockInfo(TestCase):

    ticker_list = ["BABA", "3067.HK"]
    stock_infos = AllStockInfo(ticker_list)

    def test_data_returned(self):
        for ticker in TestAllStockInfo.ticker_list:
            self.assertTrue(ticker in TestAllStockInfo.stock_infos.tickers())
        self.assertEqual(2, len(TestAllStockInfo.stock_infos.tickers()))
        self.assertEqual('ISHARESHSTECH', TestAllStockInfo.stock_infos.name('3067.HK'))

    def test_hist_price_at_date(self):
        # Test christmas public hol
        self.assertAlmostEqual(11.739999771118164,
                               TestAllStockInfo.stock_infos.price_at_date('3067.HK', datetime(2021, 12, 25).date()), 5)
        # Test weekend
        self.assertAlmostEqual(9.614999771118164,
                               TestAllStockInfo.stock_infos.price_at_date('3067.HK', datetime(2022, 7, 24).date()), 5)
        # Test at normal date 7/20
        self.assertAlmostEqual(9.640000343322754,
                               TestAllStockInfo.stock_infos.price_at_date('3067.HK', datetime(2022, 7, 20).date()), 5)
        # Test that it raises error when called before listing
        self.assertRaises(ValueError,
                          (lambda : TestAllStockInfo.stock_infos.price_at_date('3067.HK', datetime(2000, 1, 1).date())))

    def test_local_currency(self):
        self.assertEqual('USD', TestAllStockInfo.stock_infos.local_curr('BABA'))
        self.assertEqual('HKD', TestAllStockInfo.stock_infos.local_curr('3067.HK'))

    def test_invalid_ticker(self):
        ticker_list = ['Invalid ticker']
        self.assertRaises(ValueError,
                          (lambda : AllStockInfo(ticker_list)))