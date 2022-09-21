from .baseentries import single
from .baseentries import transactions
from .baseentries import atdate
from .histories import overall
from ..models import *
from datetime import datetime

def generate_transaction_list(stocktrxn_queryset):
    transaction_list = []
    for trxn in stocktrxn_queryset:
        date = trxn.date
        ticker = trxn.ticker
        quantity = trxn.quantity
        price = trxn.price
        new_transaction = transactions.StockTransaction(date, ticker, quantity, price)
        transaction_list.append(new_transaction)
    # print(transaction_list)
    return transaction_list

def generate_ownedcash_object(cashentry_object, singlecurr_queryset):
    currencies = {}
    for singlecurr in singlecurr_queryset:
        currencies[singlecurr.currency] = single.OwnedCashEntry(singlecurr.currency, singlecurr.quantity)
    cashentry_date = cashentry_object.date
    new_cashentry = atdate.OwnedCashAtDate(cashentry_date, currencies)
    return new_cashentry

def generate_cashentry_list(cashentry_queryset):
    cashentry_list = []
    for cashentry in cashentry_queryset:
        singlecurr_set = SingleCurrCashEntry.objects.filter(cash_entry=cashentry)
        new_cashentry_obj = generate_ownedcash_object(cashentry, singlecurr_set)
        cashentry_list.append(new_cashentry_obj)
    # print("THE CASH ENTRIES ARE:", cashentry_list)
    return cashentry_list

def get_analysis_across_time(ownedcash_list, stocktrxn_list, date_bef, date_aft, currency):
    overall_log = overall.OverallHistory(ownedcash_list, stocktrxn_list)
    analysis_across_time = overall_log.generate_analysis_across_time(date_bef, date_aft, currency)
    return analysis_across_time.all_statistics()

def pull_db_generate_analysis(user, date_bef, date_aft, currency):
    stocktrxns_queryset = StockTrxn.objects.filter(owner=user)
    cashentry_queryset = CashEntry.objects.filter(owner=user)
    stocktrxn_list = generate_transaction_list(stocktrxns_queryset)
    cashentry_list = generate_cashentry_list(cashentry_queryset)
    if isinstance(date_bef, str) :
        date_bef_datetime = datetime.strptime(date_bef, "%Y-%m-%d").date()
    else:
        date_bef_datetime = date_bef

    if isinstance(date_aft, str) :
        date_aft_datetime = datetime.strptime(date_aft, "%Y-%m-%d").date()
    else:
        date_aft_datetime = date_aft
    return get_analysis_across_time(cashentry_list, stocktrxn_list,
                                    date_bef_datetime, date_aft_datetime, currency)