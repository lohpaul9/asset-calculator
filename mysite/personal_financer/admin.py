from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.urls import reverse

# Add an 'edit link' to cashentry inline object for a nested inline to singleCurrCashEntry
class EditLinkToInlineObject(object):
    def Edit(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">Click to edit</a>'.format(u=url))
        else:
            return ''

class SingleCurrInline(admin.TabularInline):
    model = SingleCurrCashEntry

class CashEntryModel(admin.ModelAdmin):
    readonly_fields = ('owner', )
    inlines = (SingleCurrInline, )
    extra = 3

class CashEntryInline(EditLinkToInlineObject, admin.TabularInline):
    model = CashEntry
    readonly_fields = ('Edit',)
    extra=1

class StockTrxnInline(admin.TabularInline):
    model = StockTrxn
    fields = ('date', 'ticker', 'price', 'quantity', 'type')
    extra = 1

# class UserAdmin(admin.ModelAdmin):
#     model = User
#     inlines = (StockTrxnInline, CashEntryInline)

# Register your models here.
admin.site.register(CashEntry, CashEntryModel)

