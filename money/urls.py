from django.urls import path
from . import views

app_name = 'money'
urlpatterns = [
    path('', views.base_generic, name='base_generic'),
    path('accounts/register/', views.create_account, name='create_account'),
    path('register/', views.register, name='register'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/<wallet_id>', views.transactions_in_wallet, name='transactions_in_wallet'),
    path('add_wallet/', views.add_wallet, name='add_wallet'),
    path('add_transactions/', views.add_transaction, name='add_transaction'),
]
