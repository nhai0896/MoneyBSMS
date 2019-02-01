from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Currency(models.Model):#don vi tien te
    name = models.CharField(max_length=100)
    sign = models.CharField(max_length=5)
    ios = models.CharField(max_length=5, blank=True)
    def __str__(seft):
        return seft.name

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    inflow = models.CharField(max_length=100, default='0')
    outflow = models.CharField(max_length=100, default='0')
    balance = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    def clean(self):            
        matching_wallets = Wallet.objects.filter(name = self.name, user = self.user)
        if matching_wallets.exists():
            raise ValidationError(_('Duplicate name'))

class Category(models.Model):
    CODE = (
        ('E', 'EXPENSE'),
        ('I', 'INCOME'),
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=1, choices=CODE)
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.CharField(max_length=250)
    note = models.CharField(max_length=250, blank=True)
    time = models.DateField(default=date.today())
    def __str__(self):
        return self.note
    
