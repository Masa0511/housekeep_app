from django import forms
from django.forms.models import ModelChoiceField

from .models import(
    Income,
    Expense,
    IncomeCategories,
    ExpenseCategories,
    Account,
)

#収入入力のフォーム
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'

#支出入力のフォーム
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

#金融機関登録のフォーム
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
