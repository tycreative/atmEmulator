from django.contrib import admin

# Importing related models
from .models import Machine, Refill

# Class to display specific machine details in admin view
class MachineAdmin(admin.ModelAdmin):
    list_display = ["id", "address", "status", "minimum", "balance", "maintenance", "last_refill", "next_refill"]

# Class to display specific refill details in admin view
class RefillAdmin(admin.ModelAdmin):
    list_display = ["machine", "amount", "previous", "date_time"]

# Allow admin to modify desired models
admin.site.register(Machine, MachineAdmin)
admin.site.register(Refill, RefillAdmin)
