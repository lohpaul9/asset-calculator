from django.test import TestCase
from ..models import *
from datetime import datetime
from ..serializers import *
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer


class CashSerializerTests(TestCase):
    def setUp(self) -> None:
        CashEntry.objects.all().delete()
        data = {
            'username': 'paul1',
            'password': '12345',
        }
        serializer1 = UserCreateSerializer(data=data)
        new_user = None
        serializer1.is_valid()
        new_user = serializer1.save()

        data2 = {
            'username': 'paul2',
            'password': '12345',
        }
        serializer2 = UserCreateSerializer(data=data2)
        new_user2 = None
        serializer2.is_valid()
        new_user = serializer2.save()

    def test_creates_normal(self):
        user1 = User.objects.all()[0]
        data = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }
        serializer = CashEntrySerializer(data=data)
        serializer.is_valid()
        new_cash_entry = serializer.save(owner=user1)
        single_entries = new_cash_entry.singlecurrcashentry_set.all()
        self.assertEqual(1, len(CashEntry.objects.all()))
        self.assertEqual(3, len(single_entries))
        self.assertEqual(1, single_entries.get(currency='USD').quantity)
        self.assertEqual(2, single_entries.get(currency='SGD').quantity)
        self.assertEqual(3, single_entries.get(currency='HKD').quantity)

    def test_creates_no_clash(self):
        user1 = User.objects.all()[0]
        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 4},
                {'currency': 'SGD', 'quantity': 5},
                {'currency': 'HKD', 'quantity': 6}
            ],
        }
        serializer1 = CashEntrySerializer(data=data1)
        serializer1.is_valid()
        cash_entry1 = serializer1.save(owner=user1)
        single_entries1 = cash_entry1.singlecurrcashentry_set.all()
        serializer2 = CashEntrySerializer(data=data2)
        serializer2.is_valid()
        cash_entry2 = serializer2.save(owner=user1)
        single_entries2 = cash_entry2.singlecurrcashentry_set.all()

        self.assertEqual(2, len(CashEntry.objects.all()))
        self.assertEqual(datetime.datetime(2022, 1, 1).date(), cash_entry1.date)
        self.assertEqual(3, len(single_entries1))
        self.assertEqual(1, single_entries1.get(currency='USD').quantity)
        self.assertEqual(2, single_entries1.get(currency='SGD').quantity)
        self.assertEqual(3, single_entries1.get(currency='HKD').quantity)
        self.assertEqual(datetime.datetime(2022, 1, 2).date(), cash_entry2.date)
        self.assertEqual(3, len(single_entries2))
        self.assertEqual(4, single_entries2.get(currency='USD').quantity)
        self.assertEqual(5, single_entries2.get(currency='SGD').quantity)
        self.assertEqual(6, single_entries2.get(currency='HKD').quantity)

    def test_creates_date_clash(self):
        user1 = User.objects.all()[0]
        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 4},
                {'currency': 'SGD', 'quantity': 5},
                {'currency': 'HKD', 'quantity': 6}
            ],
        }
        serializer1 = CashEntrySerializer(data=data1)
        serializer1.is_valid()
        cash_entry1 = serializer1.save(owner=user1)
        single_entries1 = cash_entry1.singlecurrcashentry_set.all()
        serializer2 = CashEntrySerializer(data=data2)
        serializer2.is_valid()
        cash_entry2 = serializer2.save(owner=user1)
        single_entries2 = cash_entry2.singlecurrcashentry_set.all()

        self.assertEqual(1, len(CashEntry.objects.all()))
        self.assertEqual(datetime.datetime(2022, 1, 1).date(), cash_entry2.date)
        self.assertEqual(3, len(single_entries2))
        self.assertEqual(4, single_entries2.get(currency='USD').quantity)
        self.assertEqual(5, single_entries2.get(currency='SGD').quantity)
        self.assertEqual(6, single_entries2.get(currency='HKD').quantity)


    def test_update_normal(self):
        user1 = User.objects.all()[0]
        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 4},
                {'currency': 'SGD', 'quantity': 5},
                {'currency': 'HKD', 'quantity': 6}
            ],
        }
        serializer1 = CashEntrySerializer(data=data1)
        serializer1.is_valid()
        cash_entry1 = serializer1.save(owner=user1)
        serializer2 = CashEntrySerializer(cash_entry1, data=data2)
        serializer2.is_valid()
        cash_entry2 = serializer2.save(owner=user1)
        cash_entry2 = CashEntry.objects.all()[0]
        single_entries2 = cash_entry2.singlecurrcashentry_set.all()

        self.assertEqual(1, len(CashEntry.objects.all()))
        self.assertEqual(3, len(SingleCurrCashEntry.objects.all()))
        self.assertEqual(datetime.datetime(2022, 1, 2).date(), cash_entry2.date)
        self.assertEqual(3, len(single_entries2))
        self.assertEqual(4, single_entries2.get(currency='USD').quantity)
        self.assertEqual(5, single_entries2.get(currency='SGD').quantity)
        self.assertEqual(6, single_entries2.get(currency='HKD').quantity)

    def test_create_two_user(self):
        user1 = User.objects.all()[0]
        user2 = User.objects.all()[1]

        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 4},
                {'currency': 'SGD', 'quantity': 5},
                {'currency': 'HKD', 'quantity': 6}
            ],
        }
        serializer1 = CashEntrySerializer(data=data1)
        serializer1.is_valid()
        serializer1.save(owner=user1)
        cash_entries1 = CashEntry.objects.filter(owner=user1)
        single_entries1 = cash_entries1[0].singlecurrcashentry_set.all()

        serializer2 = CashEntrySerializer(data=data2)
        serializer2.is_valid()
        cash_entry2 = serializer2.save(owner=user2)
        cash_entries2 = CashEntry.objects.filter(owner=user2)
        single_entries2 = cash_entries2[0].singlecurrcashentry_set.all()

        self.assertEqual(2, len(CashEntry.objects.all()))
        self.assertEqual(6, len(SingleCurrCashEntry.objects.all()))

        self.assertEqual(datetime.datetime(2022, 1, 1).date(), cash_entries1[0].date)
        self.assertEqual(3, len(single_entries1))
        self.assertEqual(1, single_entries1.get(currency='USD').quantity)
        self.assertEqual(2, single_entries1.get(currency='SGD').quantity)
        self.assertEqual(3, single_entries1.get(currency='HKD').quantity)

        self.assertEqual(datetime.datetime(2022, 1, 1).date(), cash_entries2[0].date)
        self.assertEqual(3, len(single_entries2))
        self.assertEqual(4, single_entries2.get(currency='USD').quantity)
        self.assertEqual(5, single_entries2.get(currency='SGD').quantity)
        self.assertEqual(6, single_entries2.get(currency='HKD').quantity)

    def test_update_two_user(self):
        user1 = User.objects.get(username="paul1")
        user2 = User.objects.get(username="paul2")

        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 4},
                {'currency': 'SGD', 'quantity': 5},
                {'currency': 'HKD', 'quantity': 6}
            ],
        }
        data3 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 7},
                {'currency': 'SGD', 'quantity': 8},
                {'currency': 'HKD', 'quantity': 9}
            ],
        }
        serializer1 = CashEntrySerializer(data=data1)
        serializer1.is_valid()
        cash_entry1 = serializer1.save(owner=user1)

        serializer2 = CashEntrySerializer(data=data2)
        serializer2.is_valid()
        serializer2.save(owner=user2)

        serializer3 = CashEntrySerializer(cash_entry1, data=data3)
        serializer3.is_valid()
        serializer3.save(owner=user1)

        cash_entry1 = CashEntry.objects.get(owner=user1, date=datetime.datetime(2022, 1, 2).date())
        single_entries1 = cash_entry1.singlecurrcashentry_set.all()

        cash_entry2 = CashEntry.objects.get(owner=user2, date=datetime.datetime(2022, 1, 1).date())
        single_entries2 = cash_entry2.singlecurrcashentry_set.all()

        self.assertEqual(2, len(CashEntry.objects.all()))
        self.assertEqual(6, len(SingleCurrCashEntry.objects.all()))

        self.assertEqual(datetime.datetime(2022, 1, 2).date(), cash_entry1.date)
        self.assertEqual(3, len(single_entries1))
        self.assertEqual(7, single_entries1.get(currency='USD').quantity)
        self.assertEqual(8, single_entries1.get(currency='SGD').quantity)
        self.assertEqual(9, single_entries1.get(currency='HKD').quantity)

        self.assertEqual(datetime.datetime(2022, 1, 1).date(), cash_entry2.date)
        self.assertEqual(3, len(single_entries2))
        self.assertEqual(4, single_entries2.get(currency='USD').quantity)
        self.assertEqual(5, single_entries2.get(currency='SGD').quantity)
        self.assertEqual(6, single_entries2.get(currency='HKD').quantity)

    def test_update_two_user_clash(self):
        user1 = User.objects.get(username="paul1")
        user2 = User.objects.get(username="paul2")

        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 4},
                {'currency': 'SGD', 'quantity': 5},
                {'currency': 'HKD', 'quantity': 6}
            ],
        }
        data3 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 7},
                {'currency': 'SGD', 'quantity': 8},
                {'currency': 'HKD', 'quantity': 9}
            ],
        }
        serializer1 = CashEntrySerializer(data=data1)
        serializer1.is_valid()
        cash_entry1 = serializer1.save(owner=user1)

        serializer2 = CashEntrySerializer(data=data2)
        serializer2.is_valid()
        serializer2.save(owner=user2)

        serializer3 = CashEntrySerializer(data=data3)
        serializer3.is_valid()
        serializer3.save(owner=user1)

        cash_entry1 = CashEntry.objects.get(owner=user1, date=datetime.datetime(2022, 1, 1).date())
        single_entries1 = cash_entry1.singlecurrcashentry_set.all()

        cash_entry2 = CashEntry.objects.get(owner=user2, date=datetime.datetime(2022, 1, 1).date())
        single_entries2 = cash_entry2.singlecurrcashentry_set.all()

        self.assertEqual(2, len(CashEntry.objects.all()))
        self.assertEqual(6, len(SingleCurrCashEntry.objects.all()))

        self.assertEqual(datetime.datetime(2022, 1, 1).date(), cash_entry1.date)
        self.assertEqual(3, len(single_entries1))
        self.assertEqual(7, single_entries1.get(currency='USD').quantity)
        self.assertEqual(8, single_entries1.get(currency='SGD').quantity)
        self.assertEqual(9, single_entries1.get(currency='HKD').quantity)

        self.assertEqual(datetime.datetime(2022, 1, 1).date(), cash_entry2.date)
        self.assertEqual(3, len(single_entries2))
        self.assertEqual(4, single_entries2.get(currency='USD').quantity)
        self.assertEqual(5, single_entries2.get(currency='SGD').quantity)
        self.assertEqual(6, single_entries2.get(currency='HKD').quantity)

    def test_update_clash(self):
        user1 = User.objects.get(username="paul1")

        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 4},
                {'currency': 'SGD', 'quantity': 5},
                {'currency': 'HKD', 'quantity': 6}
            ],
        }
        data3 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 7},
                {'currency': 'SGD', 'quantity': 8},
                {'currency': 'HKD', 'quantity': 9}
            ],
        }
        serializer1 = CashEntrySerializer(data=data1)
        serializer1.is_valid()
        serializer1.save(owner=user1)

        serializer2 = CashEntrySerializer(data=data2)
        serializer2.is_valid()
        cash_entry2 = serializer2.save(owner=user1)

        serializer3 = CashEntrySerializer(cash_entry2, data=data3)
        serializer3.is_valid()
        serializer3.save(owner=user1)

        cash_entry1 = CashEntry.objects.get(owner=user1, date=datetime.datetime(2022, 1, 1).date())
        single_entries1 = cash_entry1.singlecurrcashentry_set.all()


        self.assertEqual(1, len(CashEntry.objects.all()))
        self.assertEqual(3, len(SingleCurrCashEntry.objects.all()))

        self.assertEqual(datetime.datetime(2022, 1, 1).date(), cash_entry1.date)
        self.assertEqual(3, len(single_entries1))
        self.assertEqual(7, single_entries1.get(currency='USD').quantity)
        self.assertEqual(8, single_entries1.get(currency='SGD').quantity)
        self.assertEqual(9, single_entries1.get(currency='HKD').quantity)

    def test_clash_invalid_currency(self):
        user1 = User.objects.all()[0]
        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'BLABLA', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }
        serializer1 = CashEntrySerializer(data=data1)
        with self.assertRaisesMessage(serializers.ValidationError, "BLABLA is an invalid currency"):
            serializer1.is_valid(raise_exception=True)

    def test_clash_invalid_data(self):
        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': None,
        }
        serializer1 = CashEntrySerializer(data=data1)
        with self.assertRaises(serializers.ValidationError):
            serializer1.is_valid(raise_exception=True)

        data2 = {
            'single_entries': [
            ],
        }
        serializer1 = CashEntrySerializer(data=data2)
        with self.assertRaises(serializers.ValidationError):
            serializer1.is_valid(raise_exception=True)

class StockTrxnTest(TestCase):


    def setUp(self) -> None:
        StockTrxn.objects.all().delete()
        data = {
            'username': 'paul1',
            'password': '12345',
        }
        serializer1 = UserCreateSerializer(data=data)
        new_user = None
        serializer1.is_valid()
        new_user = serializer1.save()

        data2 = {
            'username': 'paul2',
            'password': '12345',
        }
        serializer2 = UserCreateSerializer(data=data2)
        new_user2 = None
        serializer2.is_valid()
        new_user = serializer2.save()

    def test_creates_normal(self):
        user1 = User.objects.get(username='paul1')
        data = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'ticker': 'BABA',
            'quantity': 100,
            'price': 200,
            'type': 'b'
        }
        serializer1 = StockTrxnSerializer(data=data)
        serializer1.is_valid(raise_exception=True)
        serializer1.save(owner=user1)
        new_stock_trxns = StockTrxn.objects.filter(owner=user1)
        new_stock_trxn = new_stock_trxns[0]
        self.assertEqual(1, len(StockTrxn.objects.all()))
        self.assertEqual(datetime.datetime(2022, 1, 1).date(), new_stock_trxn.date)
        self.assertEqual('BABA', new_stock_trxn.ticker)
        self.assertEqual(100, new_stock_trxn.quantity)
        self.assertEqual(200, new_stock_trxn.price)
        self.assertEqual('b', new_stock_trxn.type)

    def test_creates_multiple(self):
        user1 = User.objects.get(username='paul1')
        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'ticker': 'BABA',
            'quantity': 100,
            'price': 101,
            'type': 'b'
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'ticker': 'D05.SI',
            'quantity': 200,
            'price': 201,
            'type': 'b'
        }
        serializer1 = StockTrxnSerializer(data=data1)
        serializer1.is_valid()
        serializer1.save(owner=user1)
        serializer2 = StockTrxnSerializer(data=data2)
        serializer2.is_valid()
        serializer2.save(owner=user1)
        new_stock_trxn1 = StockTrxn.objects.get(owner=user1, date=datetime.datetime(2022, 1, 1).date())
        new_stock_trxn2 = StockTrxn.objects.get(owner=user1, date=datetime.datetime(2022, 1, 2).date())

        self.assertEqual(2, len(StockTrxn.objects.all()))

        self.assertEqual(datetime.datetime(2022, 1, 1).date(), new_stock_trxn1.date)
        self.assertEqual('BABA', new_stock_trxn1.ticker)
        self.assertEqual(100, new_stock_trxn1.quantity)
        self.assertEqual(101, new_stock_trxn1.price)
        self.assertEqual('b', new_stock_trxn1.type)

        self.assertEqual(datetime.datetime(2022, 1, 2).date(), new_stock_trxn2.date)
        self.assertEqual('D05.SI', new_stock_trxn2.ticker)
        self.assertEqual(200, new_stock_trxn2.quantity)
        self.assertEqual(201, new_stock_trxn2.price)
        self.assertEqual('b', new_stock_trxn2.type)

    def test_update_multiple_same_user(self):
        user1 = User.objects.get(username='paul1')
        user2 = User.objects.get(username='paul2')

        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'ticker': 'BABA',
            'quantity': 100,
            'price': 101,
            'type': 'b'
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'ticker': 'D05.SI',
            'quantity': 200,
            'price': 201,
            'type': 'b'
        }
        data3 = {
            'date': datetime.datetime(2022, 1, 3).date(),
            'ticker': 'BABA',
            'quantity': 300,
            'price': 301,
            'type': 'b'
        }
        serializer1 = StockTrxnSerializer(data=data1)
        serializer1.is_valid()
        new_stock_trxn1 = serializer1.save(owner=user1)
        serializer2 = StockTrxnSerializer(data=data2)
        serializer2.is_valid()
        serializer2.save(owner=user1)
        serializer1 = StockTrxnSerializer(new_stock_trxn1, data=data3)
        serializer1.is_valid()
        serializer1.save(owner=user1)

        new_stock_trxn1 = StockTrxn.objects.get(owner=user1, date=datetime.datetime(2022, 1, 3).date())
        new_stock_trxn2 = StockTrxn.objects.get(owner=user1, date=datetime.datetime(2022, 1, 2).date())

        self.assertEqual(2, len(StockTrxn.objects.all()))

        self.assertEqual(datetime.datetime(2022, 1, 3).date(), new_stock_trxn1.date)
        self.assertEqual('BABA', new_stock_trxn1.ticker)
        self.assertEqual(300, new_stock_trxn1.quantity)
        self.assertEqual(301, new_stock_trxn1.price)
        self.assertEqual('b', new_stock_trxn1.type)

        self.assertEqual(datetime.datetime(2022, 1, 2).date(), new_stock_trxn2.date)
        self.assertEqual('D05.SI', new_stock_trxn2.ticker)
        self.assertEqual(200, new_stock_trxn2.quantity)
        self.assertEqual(201, new_stock_trxn2.price)
        self.assertEqual('b', new_stock_trxn2.type)


    def test_create_multiple_diff_user(self):
        user1 = User.objects.get(username='paul1')
        user2 = User.objects.get(username='paul2')

        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'ticker': 'BABA',
            'quantity': 100,
            'price': 101,
            'type': 'b'
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'ticker': 'D05.SI',
            'quantity': 200,
            'price': 201,
            'type': 'b'
        }
        data3 = {
            'date': datetime.datetime(2022, 1, 3).date(),
            'ticker': 'BABA',
            'quantity': 300,
            'price': 301,
            'type': 'b'
        }
        serializer1 = StockTrxnSerializer(data=data1)
        serializer1.is_valid()
        new_stock_trxn1 = serializer1.save(owner=user1)
        serializer2 = StockTrxnSerializer(data=data2)
        serializer2.is_valid()
        serializer2.save(owner=user2)
        serializer1 = StockTrxnSerializer(data=data3)
        serializer1.is_valid()
        serializer1.save(owner=user1)

        new_stock_trxn1 = StockTrxn.objects.get(owner=user1, date=datetime.datetime(2022, 1, 1).date())
        new_stock_trxn2 = StockTrxn.objects.get(owner=user2, date=datetime.datetime(2022, 1, 2).date())
        new_stock_trxn3 = StockTrxn.objects.get(owner=user1, date=datetime.datetime(2022, 1, 3).date())

        self.assertEqual(3, len(StockTrxn.objects.all()))
        self.assertEqual(2, len(StockTrxn.objects.filter(owner=user1)))
        self.assertEqual(1, len(StockTrxn.objects.filter(owner=user2)))

        self.assertEqual(datetime.datetime(2022, 1, 1).date(), new_stock_trxn1.date)
        self.assertEqual('BABA', new_stock_trxn1.ticker)
        self.assertEqual(100, new_stock_trxn1.quantity)
        self.assertEqual(101, new_stock_trxn1.price)
        self.assertEqual('b', new_stock_trxn1.type)

        self.assertEqual(datetime.datetime(2022, 1, 2).date(), new_stock_trxn2.date)
        self.assertEqual('D05.SI', new_stock_trxn2.ticker)
        self.assertEqual(200, new_stock_trxn2.quantity)
        self.assertEqual(201, new_stock_trxn2.price)
        self.assertEqual('b', new_stock_trxn2.type)

        self.assertEqual(datetime.datetime(2022, 1, 3).date(), new_stock_trxn3.date)
        self.assertEqual('BABA', new_stock_trxn3.ticker)
        self.assertEqual(300, new_stock_trxn3.quantity)
        self.assertEqual(301, new_stock_trxn3.price)
        self.assertEqual('b', new_stock_trxn3.type)

    def test_update_multiple_diff_user(self):
        user1 = User.objects.get(username='paul1')
        user2 = User.objects.get(username='paul2')

        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'ticker': 'BABA',
            'quantity': 100,
            'price': 101,
            'type': 'b'
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'ticker': 'D05.SI',
            'quantity': 200,
            'price': 201,
            'type': 'b'
        }
        data3 = {
            'date': datetime.datetime(2022, 1, 3).date(),
            'ticker': 'BABA',
            'quantity': 300,
            'price': 301,
            'type': 'b'
        }
        serializer1 = StockTrxnSerializer(data=data1)
        serializer1.is_valid()
        new_stock_trxn1 = serializer1.save(owner=user1)
        serializer2 = StockTrxnSerializer(data=data2)
        serializer2.is_valid()
        serializer2.save(owner=user2)
        serializer1 = StockTrxnSerializer(new_stock_trxn1, data=data3)
        serializer1.is_valid()
        serializer1.save(owner=user1)

        new_stock_trxn1 = StockTrxn.objects.get(owner=user1, date=datetime.datetime(2022, 1, 3).date())
        new_stock_trxn2 = StockTrxn.objects.get(owner=user2, date=datetime.datetime(2022, 1, 2).date())


        self.assertEqual(2, len(StockTrxn.objects.all()))
        self.assertEqual(1, len(StockTrxn.objects.filter(owner=user1)))
        self.assertEqual(1, len(StockTrxn.objects.filter(owner=user2)))

        self.assertEqual(datetime.datetime(2022, 1, 3).date(), new_stock_trxn1.date)
        self.assertEqual('BABA', new_stock_trxn1.ticker)
        self.assertEqual(300, new_stock_trxn1.quantity)
        self.assertEqual(301, new_stock_trxn1.price)
        self.assertEqual('b', new_stock_trxn1.type)

        self.assertEqual(datetime.datetime(2022, 1, 2).date(), new_stock_trxn2.date)
        self.assertEqual('D05.SI', new_stock_trxn2.ticker)
        self.assertEqual(200, new_stock_trxn2.quantity)
        self.assertEqual(201, new_stock_trxn2.price)
        self.assertEqual('b', new_stock_trxn2.type)

    # def test_valid_ticker(self):
    #     data = {
    #         'date': datetime.datetime(2022, 1, 1).date(),
    #         'ticker': 'URMAM',
    #         'quantity': 100,
    #         'price': 200,
    #         'type': 'b'
    #     }
    #     serializer1 = StockTrxnSerializer(data=data)
    #     with self.assertRaisesMessage(serializers.ValidationError,
    #                                   "URMAM is not a valid ticker in the yfinance library"):
    #         serializer1.is_valid(raise_exception=True)

    def test_create_sell_before_buy_error(self):
        user1 = User.objects.get(username='paul1')
        data1 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'ticker': 'BABA',
            'quantity': 100,
            'price': 101,
            'type': 'b'
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'ticker': 'BABA',
            'quantity': 200,
            'price': 201,
            'type': 's'
        }

        serializer1 = StockTrxnSerializer(data=data1)
        serializer1.is_valid()
        new_stock_trxn1 = serializer1.save(owner=user1)
        serializer2 = StockTrxnSerializer(data=data2)
        with self.assertRaisesMessage(serializers.ValidationError,
                                      "Earliest transaction cannot be a sell"):
            serializer2.is_valid(raise_exception=True)

    def test_update_sell_before_buy_error(self):
        user1 = User.objects.get(username='paul1')
        data1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'ticker': 'BABA',
            'quantity': 100,
            'price': 101,
            'type': 'b'
        }
        data2 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'ticker': 'BABA',
            'quantity': 200,
            'price': 201,
            'type': 's'
        }
        data3 = {
            'date': datetime.datetime(2020, 1, 1).date(),
            'ticker': 'BABA',
            'quantity': 100,
            'price': 101,
            'type': 's'
        }

        serializer1 = StockTrxnSerializer(data=data1)
        serializer1.is_valid()
        new_stock_trxn1 = serializer1.save(owner=user1)
        serializer2 = StockTrxnSerializer(data=data2)
        serializer2.is_valid()
        serializer2.save()

        serializer3 = StockTrxnSerializer(new_stock_trxn1, data=data3)
        with self.assertRaisesMessage(serializers.ValidationError,
                                      "Earliest transaction cannot be a sell"):
            serializer3.is_valid(raise_exception=True)

class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.all().delete()
        data = {
            'username': 'paul1',
            'password': '12345',
        }
        serializer1 = UserCreateSerializer(data=data)
        serializer1.is_valid()
        serializer1.save()

    def test_create_user(self):
        data = {
            'username': 'paul2',
            'password': '12345'
        }
        serializer1 = UserCreateSerializer(data=data)
        serializer1.is_valid()
        serializer1.save()
        new_user = User.objects.get(username='paul2')
        self.assertEqual('paul2', new_user.username)
        self.assertEqual(2, len(User.objects.all()))

    def test_retrieve_entries(self):
        user = User.objects.get(username='paul1')
        self.assertEqual(1, len(User.objects.all()))

        stock_data_1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'ticker': 'BABA',
            'quantity': 100,
            'price': 101,
            'type': 'b'
        }
        stock_data_2 = {
            'date': datetime.datetime(2022, 1, 2).date(),
            'ticker': 'D05.SI',
            'quantity': 200,
            'price': 201,
            'type': 'b'
        }
        stock_data_3 = {
            'date': datetime.datetime(2022, 1, 3).date(),
            'ticker': 'BABA',
            'quantity': 300,
            'price': 301,
            'type': 'b'
        }

        serializer1 = StockTrxnSerializer(data=stock_data_1)
        serializer1.is_valid()
        serializer1.save(owner=user)

        serializer2 = StockTrxnSerializer(data=stock_data_2)
        serializer2.is_valid()
        serializer2.save(owner=user)

        serializer3 = StockTrxnSerializer(data=stock_data_3)
        serializer3.is_valid()
        serializer3.save(owner=user)

        cash_data_1 = {
            'date': datetime.datetime(2022, 1, 1).date(),
            'single_entries': [
                {'currency': 'USD', 'quantity': 1},
                {'currency': 'SGD', 'quantity': 2},
                {'currency': 'HKD', 'quantity': 3}
            ],
        }

        serializer4 = CashEntrySerializer(data=cash_data_1)
        serializer4.is_valid()
        serializer4.save(owner=user)

        user = User.objects.get(username="paul1")
        user_data = UserGetSerializer(user).data
        self.assertEqual(1, len(user_data['cashentries']))
        self.assertEqual(3, len(user_data['stocktrxns']))
        self.assertEqual("paul1", user_data['username'])

