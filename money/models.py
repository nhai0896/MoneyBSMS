from django.contrib.auth.models import User
from django.db import models
from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
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
    code = models.CharField(max_length=1, choices=CODE)
    color = models.CharField(max_length=250, blank=True)
    def __str__(self):
        return self.color
    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.CharField(max_length=250)
    note = models.CharField(max_length=250, blank=True)
    time = models.DateField()
    def __str__(self):
        return self.note
    
class Language(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Category_tranlation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
