from django.contrib import admin

# Importing related models
from .models import Account, Card, Transaction

# Class to display specific account details in admin view
class AccountAdmin(admin.ModelAdmin):
    list_display = ["user", "number", "name", "phone_number", "balance"]

# Class to display specific card details in admin view
class CardAdmin(admin.ModelAdmin):
    list_display = ["account", "number", "status", "date_issued", "expiry_date"]

# Class to display specific transaction details in admin view
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "machine", "account", "date_time", "amount", "category"]

# Allow admin to modify desired models
admin.site.register(Account, AccountAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Transaction, TransactionAdmin)