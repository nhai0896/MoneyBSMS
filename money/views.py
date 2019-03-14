from django.shortcuts import render
from django.http import HttpResponse
from .models import Wallet, Category, Transaction, Currency
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from datetime import date, datetime
d = datetime.today().strftime('%Y-%m-%d')
from .sms import *

def base_generic(request):
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
        message = 'successfully!'
        return render(request, 'registration/login.html')
    except (IntegrityError): 
        message = 'account existed!'
        return render(request, 'registration/login.html')
    
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
            'date': d,
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
        'date': d,
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
        w = Wallet(user=request.user, name=name, currency=cur, balance=balance, inflow=balance)
        w.save()
        lcategory = Category.objects.filter(name='Others_Income').get()
        t = Transaction(wallet = w, amount=balance, category=lcategory, time=d)
        t.save()
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
    #wallet = Wallet.objects.filter(user=request.user).exclude(name=request.POST['wallet']).get()
    wallet = Wallet.objects.filter(name=request.POST['wallet']).get(user=request.user)
    #name=request.POST.get('category', False)
    #print(name)
    note = request.POST['note']
    time = request.POST['time']
    #userId = request.user.username
    t = Transaction(wallet = wallet, amount=amount, category=lcategory, note=note, time=time)
    if lcategory.code == 'E':
        wallet.balance = str(int(wallet.balance) - int(amount))
        wallet.outflow = str(int(amount) + int(wallet.outflow))
    elif lcategory.code == 'I':
        wallet.balance = str(int(amount) + int(wallet.balance))
        wallet.inflow = str(int(amount) + int(wallet.inflow))
    #w.user_username=username
    #print(username)
    #print(w.User)
    t.save()
    wallet.save()
    return redirect('money:transactions_in_wallet', wallet.id)

def add_message(request):
    messag = request.POST.get('message', False)
    wallet = Wallet.objects.filter(user=request.user).exclude(name=request.POST['wallet']).get()
    n = messag.split("\r\n")
    message = ' '.join(n)
    i = -1;
    m = re.search(bank, message)

    if m:
        if m.group() == 'BIDV':
            i = 0
        elif m.group() == 'VietinBank':
            i = 1
        elif m.group() == 'Ref':
            i = 2
        elif m.group() == 'TPBank':
            i = 3
        elif m.group() == 'Agribank':
            i = 4
    Message(message, i)
    lcategory = Category.objects.get(name=result['Category'])
    t = Transaction(wallet = wallet, amount=result['Amount'], category=lcategory, note=result['Note'], time=result['Time'])
    if lcategory.code == 'E':
        wallet.balance = str(int(wallet.balance) - int(result['Amount']))
        wallet.outflow = str(int(result['Amount']) + int(wallet.outflow))
    elif lcategory.code == 'I':
        wallet.balance = str(int(result['Amount']) + int(wallet.balance))
        wallet.inflow = str(int(result['Amount']) + int(wallet.inflow))
    t.save()
    wallet.save()
    return redirect('money:transactions_in_wallet', wallet.id)


def delete_or_edit(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    wallet = Wallet.objects.filter(transaction__id=transaction_id).get()
    if transaction.category.code == 'E':
            wallet.balance = str(int(wallet.balance) + int(transaction.amount))
            wallet.outflow = str(int(wallet.outflow) - int(transaction.amount))
    elif transaction.category.code == 'I':
        wallet.balance = str(int(wallet.balance) - int(transaction.amount))
        wallet.inflow = str(int(wallet.inflow) - int(transaction.amount))
    if 'yes' in request.POST:
        wallet.save()
        transaction.delete()
        return redirect('money:transactions_in_wallet', wallet.id)
    elif 'save' in request.POST:
        transaction.amount = request.POST['amount']
        lcategory = Category.objects.get(name=request.POST['category'])
        transaction.category = lcategory
        transaction.note = request.POST['note']
        transaction.time = request.POST['time']
        
        if lcategory.code == 'E':
            wallet.balance = str(int(wallet.balance) - int(transaction.amount))
            wallet.outflow = str(int(transaction.amount) + int(wallet.outflow))
        elif lcategory.code == 'I':
            wallet.balance = str(int(transaction.amount) + int(wallet.balance))
            wallet.inflow = str(int(transaction.amount) + int(wallet.inflow))
            
        transaction.save()
        wallet.save()
        return redirect('money:transactions_in_wallet', wallet.id)

def delete_or_edit_wallet(request, wallet_id):
    wallet = Wallet.objects.get(pk=wallet_id)
    if 'yes' in request.POST:
        wallet.delete()
        return redirect('money:transactions')
    elif 'save' in request.POST:
        wallet.name = request.POST['name']
        wallet.currency = Currency.objects.get( name=request.POST['currency'])
        a = True
        all_wallets = Wallet.objects.filter(user=request.user.id)
        for w in all_wallets:
            if wallet.name == w.name:
                a = False
                break
        if a:
            wallet.save()
        return redirect('money:transactions_in_wallet', wallet.id)
    
# Chart.js
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

class ChartData(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        
        #unicode(request.user)
        categ_amount= Transaction.objects.filter(wallet__user=request.user.id).values('category').order_by('category').annotate(total_amount=Sum('amount'))
        
        #categ_amount = Transaction.objects.values('category').order_by('category').annotate(total_amount=Sum('amount'))
        
        #print(request.user)
        #print(categ_amount)
        
        labels = []
        color = []
        default_items = []
        #fruits.append("orange")
        for c in categ_amount:
            default_items.append(c['total_amount'])
            cate = Category.objects.get(pk=c['category'])
            labels.append(cate.name)
            color.append(cate.color)
        
        data = {
                "labels": labels,
                "default": default_items,
                "color": color,
        }
        return Response(data)
    
	
	
	
	



















































