

class OwnedStockEntry:
    def __init__(self, ticker:str, quantity:float, price:float):
        self.ticker = ticker
        self.quantity = quantity
        self.price = price

    def handle_transaction(self, trxn):
        if self.ticker != trxn.ticker:
            raise ValueError
        match trxn.type:
            case 'b':
                self.price = (self.price * self.quantity + trxn.price * trxn.quantity) \
                             / (trxn.quantity + self.quantity)
                self.quantity = trxn.quantity + self.quantity
            case 's':
                self.quantity = self.quantity - trxn.quantity

    def __repr__(self):
        return f"OwnedStockEntry: {self.ticker} price: {self.price} qty: {self.quantity}"

class OwnedCashEntry:
    def __init__(self, currency : str, quantity : float):
        self.currency = currency
        self.quantity = quantity

    def __repr__(self):
        return f"OwnedCashEntry: {self.currency} {self.quantity}"