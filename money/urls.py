from django.urls import path
from . import views

#from .views import ChartDataWallet

app_name = 'money'
urlpatterns = [
    path('', views.base_generic, name='base_generic'),
    path('accounts/register/', views.create_account, name='create_account'),
    path('register/', views.register, name='register'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/<wallet_id>', views.transactions_in_wallet, name='transactions_in_wallet'),
    path('add_wallet/', views.add_wallet, name='add_wallet'),
    path('add_transactions/', views.add_transaction, name='add_transaction'),
    path('delete_or_edit/<transaction_id>', views.delete_or_edit, name='delete_or_edit'),
    path('delete_or_edit_wallet/<wallet_id>', views.delete_or_edit_wallet, name='delete_or_edit_wallet'),
    path('add_message/', views.add_message, name='add_message'),
    path('increment_month/', views.increment_month, name='increment_month'),
    path('decrement_month/', views.decrement_month, name='decrement_month'),
    path('inc_month/<wallet_id>', views.inc_month, name='inc_month'),
    path('dec_month/<wallet_id>', views.dec_month, name='dec_month'),
   # path('chart/', views.chart, name='chart'),
]



