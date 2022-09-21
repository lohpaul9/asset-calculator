import logging
from _datetime import datetime
import yfinance as yf
from .scraper import *

#
class StockInfo:
    def __init__(self, ticker, gen_info, hist_price):
        self.ticker = ticker
        self.gen_info = gen_info
        # Hist price is of the format sorted [datetimeObj] -> closingPrice
        self.hist_price = hist_price

    def name(self):
        return self.gen_info['shortName']

    def currPrice(self):
        return self.gen_info['regularMarketPrice']

    def currency(self):
        return self.gen_info['currency']

    def get_gen_info(self):
        return self.gen_info.copy()

    def __repr__(self):
        return f"StockInfoObj {self.ticker}"

    def priceAtDate(self, date):
        """
        returns the price at a given date. If market is closed on that day, returns
        the closest historical price before that. If no valid price before that, (ie
        stock is not listed then) ValueError is raised

        :param date: datetime Obj
        :return: price in stock exchange curr
        """
        if (date == datetime.today().date()):
            return self.currPrice()

        max = len(self.hist_price) - 1
        founddate = False
        while (max >= 0):
            # print("Printing the value of histprice indexed", self.histPrice[max])
            if self.hist_price[max][0].date() <= date:
                return self.hist_price[max][1]

            max = max - 1
        print("Can't find valid number to date!")
        raise ValueError


class AllStockInfo():
    def __init__(self, ticker_list: list[str]):
        scraper = YFinScraper()
        # Generate all general info
        gen_info_dict = {}
        for ticker in ticker_list:
            gen_info_dict[ticker] = scraper.get_general_stock_info(ticker)

        # Generate all historical prices
        hist_price_dict = scraper.find_hist_price(ticker_list)

        # Create dict of StockInfo objects
        all_info = {}
        for ticker in gen_info_dict:
            all_info[ticker] = StockInfo(ticker, gen_info_dict[ticker], hist_price_dict[ticker])
        self.all_info = all_info

    def price_at_date(self, ticker: str, date: datetime):
        return self.all_info[ticker].priceAtDate(date)

    def local_curr(self, ticker: str):
        return self.all_info[ticker].currency()

    def gen_info(self, ticker: str):
        return self.all_info[ticker].get_gen_info()

    def tickers(self):
        return self.all_info.keys()

    def name(self, ticker: str):
        return self.all_info[ticker].name()
