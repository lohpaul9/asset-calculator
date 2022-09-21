from django.db import models
from django.core.exceptions import ValidationError
from currency_converter import CurrencyConverter
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your models here.
class StockTrxn(models.Model):
    owner = models.ForeignKey('auth.User',related_name='stocktrxns', on_delete=models.CASCADE)
    date = models.DateField()
    ticker = models.CharField(max_length=40)
    quantity = models.IntegerField()
    price = models.FloatField()
    type = models.CharField(max_length=1)

    class Meta:
        ordering = ['date']

    def __repr__(self):
        return f"StockTrxn: {self.owner.username} {self.date} {self.ticker} {self.quantity} @ {self.price}"

class CashEntry(models.Model):
    owner = models.ForeignKey('auth.User', related_name='cashentries', on_delete=models.CASCADE)
    date = models.DateField()

    def __repr__(self):
        return f"CashEntry: {self.date}"

    class Meta:
        ordering = ['date']

class SingleCurrCashEntry(models.Model):
    currency = models.CharField(max_length=10)
    quantity = models.FloatField()
    cash_entry = models.ForeignKey(CashEntry, on_delete=models.CASCADE)

    def __repr__(self):
        return f"CashEntry: {self.currency} {self.quantity}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
