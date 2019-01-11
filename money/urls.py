from django.urls import path
from . import views

app_name = 'money'
urlpatterns = [
    path('', views.base_generic, name='base_generic'),
    path('accounts/register_form/', views.register, name='register'),
    path('accounts/register/', views.create_account, name='create_account'),
    path('transactions/', views.transactions, name='transactions'),
    path('add_wallet/', views.add_wallet, name='add_wallet'),
    path('logged_out/', views.logout_view, name='logout_view'),
    path('add_transactions/', views.add_transaction, name='add_transaction'),
]