from django.contrib.auth.models import User
from django.db import models
from datetime import date

# Create your models here.

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=250) #don vi tien te
    inflow = models.CharField(max_length=100, default='0')
    outflow = models.CharField(max_length=100, default='0')
    balance = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
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
    note = models.CharField(max_length=250)
    time = models.DateField(default=date.today())
    def __str__(self):
        return self.note
    
