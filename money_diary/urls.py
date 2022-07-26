from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('monthly_details/', views.Monthly_DetailsView.as_view(), name='monthly_details'),
    path('monthly_details/<int:year>/<int:month>', views.Monthly_DetailsView.as_view(), name='monthly_details'),
    path('by_account/', views.By_AccountView.as_view(), name='by_account'),
    path('assets/', views.AssetsView.as_view(), name='assets'),
    path('setup/', views.SetupView.as_view(), name='setup'),
    path('income_delete/<int:num>', views.Income_DeleteView, name='income_delete'),
    path('expense_delete/<int:num>', views.Expense_DeleteView, name='expense_delete'),
    path('account_detail/<int:num>', views.Account_DetailView.as_view(), name='account_detail'),
    path('account_detail/<int:num>/<int:year>/<int:month>', views.Account_DetailView.as_view(), name='account_detail'),
]
