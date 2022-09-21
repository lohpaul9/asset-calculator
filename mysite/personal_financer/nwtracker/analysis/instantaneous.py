from ..assets.nwatdate import NwAtDate
from ..yfinscrape.allstockinfo import AllStockInfo
from ..baseentries.atdate import Dated
from currency_converter import CurrencyConverter

class AnalysisInstantaneous(Dated):
    def __init__(self, stock_info: AllStockInfo, currency: str, converter: CurrencyConverter, nw: NwAtDate):
        self.stock_info = stock_info
        self.currency = currency
        self.nw = nw
        self.date = nw.date
        self.converter = converter

    # Generates value for all stocks
    def stock_value(self):
        total_value = 0
        # print(f"--CALCULATING STOCK VALUES OWNED AT {self.date}--")
        for ticker in self.nw.all_stocks():
            val_conv_curr = self.single_stock_value(ticker)
            total_value += val_conv_curr
        # print(f"TOTAL = {total_value} {self.currency}\n")
        return total_value

    def single_stock_value(self, ticker):
        stock = self.nw.all_stocks()[ticker]
        local_curr = self.stock_info.local_curr(stock.ticker)
        val_local_curr = stock.quantity * self.stock_info.price_at_date(stock.ticker, self.date)
        val_conv_curr = self.converter.convert(val_local_curr, local_curr, self.currency)
        # print(f"""{stock.ticker}  qty:{stock.quantity} * prc:{self.stock_info.price_at_date(stock.ticker, self.date)} =  {val_local_curr} {local_curr} = {val_conv_curr} {self.currency}""")
        return val_conv_curr

    def cash_value(self):
        total_cash = 0
        # print(f"--CALCULATING CASH VALUES OWNED AT {self.date}--")
        for currency in self.nw.all_cash():
            val_conv_curr = self.single_cash_value(currency)
            total_cash += val_conv_curr
        # print(f"TOTAL CASH {total_cash} {self.currency}\n")
        return total_cash

    def single_cash_value(self, currency):
        cash_entry = self.nw.all_cash()[currency]
        val_conv_curr = self.converter.convert(cash_entry.quantity, cash_entry.currency, self.currency)
        # print(f"HOLDING {cash_entry.quantity}{cash_entry.currency} == {val_conv_curr}{self.currency}")
        return val_conv_curr

    def total_value(self):
        return self.cash_value() + self.stock_value()

    def stocks_bought_value(self):
        total_value = 0
        # print(f"--CALCULATING AVG STOCK BOUGHT PRICE FOR {self.date}--")
        for ticker in self.nw.all_stocks():
            val_conv_curr = self.single_stock_bought_value(ticker)
            total_value += val_conv_curr
        # print(f"TOTAL = {total_value} {self.currency}\n")
        return total_value

    def single_stock_bought_value(self, ticker):
        stock = self.nw.all_stocks()[ticker]
        local_curr = self.stock_info.local_curr(ticker)
        val_local_curr = stock.quantity * stock.price
        val_conv_curr = self.converter.convert(val_local_curr, local_curr, self.currency)
        # print(
        #     f"""{stock.ticker}  qty:{stock.quantity} * boughtprc:{stock.price} =  {val_local_curr} {local_curr} = {val_conv_curr} {self.currency}""")
        return val_conv_curr

