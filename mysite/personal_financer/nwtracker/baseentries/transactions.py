from datetime import datetime
from .atdate import Dated

class StockTransaction(Dated):
    def __init__(self, date : datetime.date, ticker : str, quantity : int, price : int, type = 'b') -> None:
        self.date = date
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.type = type

    def __repr__(self):
        return f"StockEntryObj: {self.ticker} qty: {self.quantity}, prc: {self.price} date: {self.date.strftime('%d/%m/%Y')} "

