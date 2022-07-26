from django.contrib import admin

from .models import (
    Income,
    Expense,
    Account,
    AccountBalance,
    AccountHis,
    Assets,
    IncomeCategories,
    ExpenseCategories,
)

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Account)
admin.site.register(Assets)
admin.site.register(IncomeCategories)
admin.site.register(ExpenseCategories)
admin.site.register(AccountBalance)
admin.site.register(AccountHis)
