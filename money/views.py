from django.shortcuts import render
from django.http import HttpResponse
from .models import Wallet, Category, Transaction, Currency
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from datetime import date, datetime
from .sms import *

def base_generic(request):
    #return 0 cac ham lien ket trong url phai tra ve httpresponse 
    if request.user.is_authenticated:
        return redirect('money:transactions')
    else:
        return render(request, 'base_generic.html')
def register(request):
    return render(request, 'registration/register.html')

from django.db import IntegrityError

def create_account(request):
    username = request.POST['username']#neu dung id cua label thi: request.POST.get('usernemr', False)
    password = request.POST['password']
    try:
        user = User.objects.create_user(username=username, password=password)
        return render(request, 'registration/login.html')
    except (IntegrityError): 
        return render(request, 'registration/register.html')
    
from django.core.exceptions import ObjectDoesNotExist

currency = Currency.objects.all()
category = Category.objects.all()
def transactions(request):#login_view all_wallets
    username = request.user.username
    all_wallets = Wallet.objects.filter(user=request.user.id)
    #Entry.objects.filter(blog__name='Beatles Blog')
    if len(all_wallets) != 0:
        all_transactions = Transaction.objects.filter(wallet__user__id=request.user.id)
        class Wallets:
            inflow = '0'
            balance = '0'
            outflow = '0'
        wallet = Wallets()
        for w in all_wallets:
            wallet.balance = str(int(wallet.balance) + int(w.balance))
            wallet.inflow = str(int(wallet.inflow) + int(w.inflow))
            wallet.outflow = str(int(wallet.outflow) + int(w.outflow))
        context = {
            'username':username,
            'wallet': wallet,
            'all_transactions': all_transactions,
            'category': category,
            'all_wallets': all_wallets,
            'in_wallet':'All wallets',
            'currency': currency,
            'bank': bank,
        }
        return render(request, 'money/transactions.html', context)
    else:
        context = {
            'username':username,
            'currency': currency,
        }
        return render(request, 'money/wallet.html', context)
    
def transactions_in_wallet(request, wallet_id):
    username = request.user.username
    all_wallets = Wallet.objects.filter(user=request.user.id)
    wallet = Wallet.objects.get(pk=wallet_id)
    #Entry.objects.filter(blog__name='Beatles Blog')
    all_transactions = Transaction.objects.filter(wallet=wallet_id)
    context = {
        'username':username,
        'wallet': wallet,
        'all_transactions': all_transactions,
        'category': category,
        'all_wallets': all_wallets,
        'in_wallet': wallet.name,
        'wallet_id': int(wallet_id),
        'currency': currency,
        'bank': bank,
    }
    return render(request, 'money/transactions.html', context)
    
def add_wallet(request):
    username = request.user.username
    name = request.POST['name']
    cur = Currency.objects.get( name=request.POST['currency'])
    balance = request.POST['balance']
    #userId = request.user.username
    a = True
    all_wallets = Wallet.objects.filter(user=request.user.id)
    for wallet in all_wallets:
        if name == wallet.name:
            a = False
            break
    if a:
        w = Wallet(user=request.user, name=name, currency=cur, balance=balance)
        #w.user_username=username
        #print(username)
        #print(w.User)
        w.save()
        return redirect('money:transactions_in_wallet', w.id)
    else:
        context = {
            'username':username,
            'currency': currency,
        }
        return render(request,'money/wallet.html', context)
        
    
def add_transaction(request):
    amount = request.POST['amount']
    lcategory = Category.objects.get(name=request.POST['category'])
    wallet = Wallet.objects.filter(name=request.POST['wallet']).filter(user=request.user).get()
    #name=request.POST.get('category', False)
    #print(name)
    note = request.POST['note']
    time = request.POST['time']
    #tim = time.split("-")
    #date = datetime.date(int(tim[2]), int(tim[0]), int(tim[1]))
    t = Transaction(wallet = wallet, amount=amount, category=lcategory, note=note, time=time)
    if lcategory.code == 'E':
        wallet.balance = str(int(wallet.balance) - int(amount))
        wallet.outflow = str(int(amount) + int(wallet.outflow))
    else:
        wallet.balance = str(int(amount) + int(wallet.balance))
        wallet.inflow = str(int(amount) + int(wallet.inflow))
    #w.user_username=username
    #print(username)
    #print(w.User)
    t.save()
    wallet.save()
    return redirect('money:transactions_in_wallet', wallet.id)

def add_message(request):
    return render(request, 'money/wallets.html')
    


































