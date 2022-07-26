from apscheduler.schedulers.background import BackgroundScheduler
from .models import Account, AccountBalance, AccountHis

#定期実行の処理
def update():
    account = Account.objects.values_list('name', flat=True)

    for name in account:
        account = AccountBalance.objects.all().filter(name__name=name).latest('date')

        AccountHis.objects.create(
            name = account.name,
            balance = account.balance
        )

    print('更新')

#定期実行のインターバル設定
def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(update, 'cron', hour=0)
    scheduler.start()
