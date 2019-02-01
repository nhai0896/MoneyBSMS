from django.urls import path
from . import views

app_name = 'money'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('accounts/register/', views.create_account, name='create_account'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/<wallet_id>', views.transactions_in_wallet, name='transactions_in_wallet'),
    path('add_wallet/', views.add_wallet, name='add_wallet'),
    path('add_transactions/', views.add_transaction, name='add_transaction'),

    path('add_wl/', views.add_wl, name='add_wl'),
]
