from datetime import datetime
from .single import OwnedCashEntry, OwnedStockEntry

class Dated:
    def __init__(self, date:datetime.date):
        self.date = date

    def rounded_date(self):
        return self.date

class OwnedAssetsAtDate(Dated):
    def __init__(self, date:datetime.date, entries: dict):
        self.date = date
        self.entries = entries

    def get_assets(self) -> dict:
        return self.entries.copy()


class OwnedCashAtDate(OwnedAssetsAtDate):
    def __init__(self, date : datetime.date, cash_entries : dict[str, OwnedCashEntry]):
        super().__init__(date, cash_entries)

    def __repr__(self):
        str = f'OwnedCashAtDate: {self.date.strftime("%m/%d/%Y")} :'
        for owned_cash in self.entries.values():
            str += f"\n{owned_cash}"
        return str


class OwnedStockAtDate(OwnedAssetsAtDate):
    def __init__(self, date : datetime.date, stock_entries : dict[str, OwnedStockEntry]):
        super().__init__(date, stock_entries)

    def __repr__(self):
        str = f'OwnedStockAtDate: {self.date.strftime("%m/%d/%Y")} :'
        for stock in self.entries.values():
            str += f"\n{stock}"
        return str
