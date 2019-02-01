from django import forms
from .models import Wallet, Currency
from django import forms

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'currency', 'balance', 'user']