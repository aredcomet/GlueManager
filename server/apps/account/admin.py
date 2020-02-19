from django.contrib import admin

from apps.account.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass
