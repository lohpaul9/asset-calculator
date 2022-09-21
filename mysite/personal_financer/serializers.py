import datetime
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import StockTrxn, CashEntry, SingleCurrCashEntry
from django.contrib.auth.models import User
from currency_converter import CurrencyConverter
import yfinance as yf

class StockTrxnSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = StockTrxn
        fields = ['id', 'date', 'ticker', 'quantity', 'price', 'type', 'owner']

    # def validate_ticker(self, ticker):
    #     stock_data = yf.Ticker(ticker).info
    #     if stock_data.get('regularMarketPrice', None) == None :
    #         raise serializers.ValidationError(f"{ticker} is not a valid ticker in the yfinance library")
    #     return ticker

    def validate_type(self, type):
        if type not in ["b", "s"]:
            raise serializers.ValidationError(f"transaction type must be 'b' or 's'")
        return type

    def validate(self, data):
        if data["type"] == "s":
            same_ticker_trxn = StockTrxn.objects.filter(date__lte=data["date"])
            for trxn in same_ticker_trxn:
                if trxn.type == "b":
                    return data
            raise serializers.ValidationError(f"Earliest transaction cannot be a sell")
        return data

class SingleCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleCurrCashEntry
        fields = ['currency', 'quantity']

    def validate_currency(self, currency):
        c = CurrencyConverter()
        if currency not in c.currencies:
            raise serializers.ValidationError(f"{currency} is an invalid currency")
        else:
            return currency

class CashEntrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    single_entries = SingleCashSerializer(many=True, source='singlecurrcashentry_set')

    class Meta:
        model = CashEntry
        fields = ['id', 'date', 'single_entries','owner']

    # Creating a cash entry just creates it for all
    def create(self, validated_data):
        CashEntry.objects.filter(date=validated_data['date'], owner=validated_data['owner']).delete()
        single_entry_data = validated_data.pop('singlecurrcashentry_set')
        cash_entry = CashEntry.objects.create(**validated_data)
        for single_entry in single_entry_data:
            SingleCurrCashEntry.objects.create(**single_entry, cash_entry=cash_entry)
        return cash_entry

    # Updating a cash entry will 'refresh' by deleting the current set and adding the new set
    def update(self, instance, validated_data):
        CashEntry.objects.filter(date=validated_data['date'], owner=validated_data['owner']).delete()
        instance.date = validated_data.get('date', instance.date)
        SingleCurrCashEntry.objects.filter(cash_entry=instance).delete()
        single_entry_data = validated_data.pop('singlecurrcashentry_set')
        for single_entry in single_entry_data:
            SingleCurrCashEntry.objects.create(**single_entry, cash_entry=instance)
        instance.save()
        return instance

class UserGetSerializer(serializers.ModelSerializer):
    stocktrxns = serializers.PrimaryKeyRelatedField(many=True, queryset=StockTrxn.objects.all())
    cashentries = serializers.PrimaryKeyRelatedField(many=True, queryset=CashEntry.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'stocktrxns', 'cashentries']

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_username(self, username):
        all_users = User.objects.filter(username=username)
        if len(all_users) > 0:
            raise serializers.ValidationError("username already taken")
        else:
            return username

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

class AnalysisAcrossRequestSerializer(serializers.Serializer):
    date_bef = serializers.DateField()
    date_aft = serializers.DateField()
    currency = serializers.CharField(max_length=10)

    def validate_currency(self, currency):
        c = CurrencyConverter()
        if currency not in c.currencies:
            raise serializers.ValidationError(f"{currency} is an invalid currency")
        else:
            return currency

    def validate(self, data):
        if data["date_bef"] > data["date_aft"]:
            raise serializers.ValidationError("date_bef cannot be after date_aft")
        return data

class AnalysisAcrossResponseSerializer(serializers.Serializer):
    raw_total_growth = serializers.FloatField()
    percent_total_growth = serializers.FloatField()
    raw_portfolio_growth = serializers.FloatField()
    raw_profit_and_loss = serializers.FloatField()
    raw_non_market_growth = serializers.FloatField()

    class Meta:
        fields = ["raw_total_growth", "percent_total_growth", "raw_portfolio_growth", "raw_profit_and_loss", "raw_non_market_growth"]