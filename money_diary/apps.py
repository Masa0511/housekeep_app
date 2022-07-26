from django.apps import AppConfig

class MoneyDiaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'money_diary'
    
    def ready(self):
        """起動時に呼び出される"""
        from .update import start
        start()
