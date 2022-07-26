from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone

from .models import Income, Expense, Account, AccountBalance, Assets, IncomeCategories, ExpenseCategories, AccountHis
from .forms import IncomeForm, ExpenseForm, AccountForm

today = str(timezone.now()).split('-') #今日の日付

#トップページ
class IndexView(View):
    def get(self, request):
        #データをインスタンスに格納
        income = Income.objects.all()
        expense = Expense.objects.all()

        #formをインスタンスに格納
        incomeform = IncomeForm()
        expenseform = ExpenseForm()

        params = {
            'income': income,
            'expense': expense,
            'incomeform': incomeform,
            'expenseform': expenseform,
        }
        return render(request, 'money_diary/index.html', params)

    def post(self, request):
        #収入の登録が行われた時
        if 'income_register_button' in request.POST:
            #収入をデータベースに追加
            income = Income()
            incomeform = IncomeForm(request.POST, instance=income)
            incomeform.save()

            #口座の最新残高をデータベースに追加

            last_balance = AccountBalance.objects.filter(name=income.account).values_list('balance', flat=True).last()
            latest_balance = int(last_balance) + income.amount
            AccountBalance.objects.create(
                name = income.account,
                balance = latest_balance
            )


        #支出の登録が行われた時
        elif 'expense_register_button' in request.POST:
            #収入をデータベースに追加
            expense = Expense()
            expenseform = ExpenseForm(request.POST, instance=expense)
            expenseform.save()

            #口座の最新残高をデータベースに追加
            last_balance = AccountBalance.objects.filter(name=expense.account).values_list('balance', flat=True).last()
            latest_balance = int(last_balance) - expense.amount
            AccountBalance.objects.create(
                name = expense.account,
                balance = latest_balance
            )

        return redirect(to='/')

#月別詳細
class Monthly_DetailsView(View):
    def get(self, request, year=int(today[0]), month=int(today[1])):
        #指定月の収支データを取得
        income = Income.objects.filter(date__year=year, date__month=month).order_by('-date')
        expense = Expense.objects.filter(date__year=year, date__month=month).order_by('-date')

        #輸入、支出の合計を取得
        income_total = 0
        for item in income:
            income_total += item.amount

        expense_total = 0
        for item in expense:
            expense_total += item.amount

        #収支の計算
        balance_payment = income_total - expense_total

        if month == 12:
            last_year = year
            last_month = 11
            next_year = year + 1
            next_month = 1
        elif month == 1:
            last_year = year - 1
            last_month = 12
            next_year = year
            next_month = 2
        else:
            last_year = year
            last_month = month - 1
            next_year = year
            next_month = month + 1

        params = {
            'year': year,
            'month': month,
            'last_year': last_year,
            'last_month': last_month,
            'next_year': next_year,
            'next_month': next_month,
            'income': income,
            'income_total': income_total,
            'expense': expense,
            'expense_total': expense_total,
            'balance_payment': balance_payment,
        }

        return render(request, 'money_diary/monthly_details.html', params)

def Income_DeleteView(self, num):
    income = Income.objects.get(id=num)
    income.delete()
    return redirect(to='/monthly_details')

def Expense_DeleteView(self, num):
    expense = Expense.objects.get(id=num)
    expense.delete()
    return redirect(to='/monthly_details')

class By_AccountView(View):
    def get(self, request):
        account = Account.objects.all()

        #口座名のリストを作成
        account_name = []
        for n in account:
            account_name.append(n.name)

        #各口座の最新クエリをリストに追加
        account_balance = []
        for i in account_name:
            latest_account = AccountBalance.objects.filter(name__name=i).latest('date')
            account_balance.append(latest_account)

        params = {
            'account_balance': account_balance,

        }

        return render(request, 'money_diary/by_account.html', params)

class AssetsView(View):
    def get(self, request):

        params = {

        }

        return render(request, 'money_diary/assets.html', params)

#設定画面の処理
class SetupView(View):
    def get(self, request):

        accountform = AccountForm()

        params = {
            'accountform': accountform,
        }

        return render(request, 'money_diary/setup.html', params)

    def post(self, request):
        if 'account' in request.POST:
            account = Account()
            accountform = AccountForm(request.POST, instance=account)
            accountform.save()

            AccountBalance.objects.create(
                name = account,
                balance = account.balance
            )

        return redirect(to='/setup')

class Account_DetailView(View):
    def get(self, request, num, year=int(today[0]), month=int(today[1])):
        # 選択口座のデータの取得
        account = AccountBalance.objects.get(id=num)
        # 選択講座の収支データの取得
        income = Income.objects.all().filter(account__name=account.name, date__year=year, date__month=month).order_by()
        expense = Expense.objects.all().filter(account__name=account.name, date__year=year, date__month=month).order_by()

        #グラフのデータ取得
        account_his = AccountHis.objects.all().filter(name=account.name)

        balance = []
        date = []

        #グラフ用データをリストに格納
        for n in account_his:
            date.append(n.date.strftime('%y/%m/%d'))
            balance.append(n.balance)

        # 月次切り替えの際の条件
        if month == 12:
            last_year = year
            last_month = 11
            next_year = year + 1
            next_month = 1
        elif month == 1:
            last_year = year - 1
            last_month = 12
            next_year = year
            next_month = 2
        else:
            last_year = year
            last_month = month - 1
            next_year = year
            next_month = month + 1

        params = {
            'account': account,
            'income': income,
            'expense': expense,
            'date': date,
            'balance': balance,
            'year': year,
            'month': month,
            'last_year': last_year,
            'last_month': last_month,
            'next_year': next_year,
            'next_month': next_month,
        }

        return render(request, 'money_diary/account_detail.html', params)
