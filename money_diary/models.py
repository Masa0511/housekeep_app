from django.db import models
from django.utils import timezone

#口座のモデル
class Account(models.Model):
    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=20) #口座名
    balance = models.IntegerField() #初期登録残高

    def __str__(self):
        return self.name

#口座の残高モデル
class AccountBalance(models.Model):
    date = models.DateField(default=timezone.now)
    name = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.IntegerField()

    def __str__(self):
        return str(self.date) +'_' + self.name.name

#一定間隔の各口座残高
class AccountHis(models.Model):
    date = models.DateField(default=timezone.now)
    name = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.IntegerField()

    def __str__(self):
        return str(self.date) +'_' + self.name.name


#収入のカテゴリー
class IncomeCategories(models.Model):
    name = models.CharField(max_length=30) #収入カテゴリーの名前

    def __str__(self):
        return self.name

#収入のモデル
class Income(models.Model):
    date = models.DateField(default=timezone.now) #日付
    category = models.ForeignKey(IncomeCategories, on_delete=models.CASCADE) #カテゴリ
    account = models.ForeignKey(Account, on_delete=models.CASCADE) #入金口座
    amount = models.IntegerField() #金額
    memo = models.TextField(null=True, blank=True, max_length=100) #メモ

    def __str__(self):
        return self.category.name + str(self.amount)

#支出のカテゴリー
class ExpenseCategories(models.Model):
    name = models.CharField(max_length=30) #支出カテゴリーの名前

    def __str__(self):
        return self.name

#支出のモデル
class Expense(models.Model):
    date = models.DateField(default=timezone.now) #日付
    category = models.ForeignKey(ExpenseCategories, on_delete=models.CASCADE) #カテゴリ
    account = models.ForeignKey(Account, on_delete=models.CASCADE) #出所
    amount = models.IntegerField() #金額
    memo = models.TextField(null=True, blank=True, max_length=100) #メモ

    def __str__(self):
        return self.category.name + str(self.amount)



#資産推移のモデル
class Assets(models.Model):
    date = models.DateTimeField(default=timezone.now) #日付
    amount = models.IntegerField() #資産総額

    def __str__(self):
        return self.date + self.amount
