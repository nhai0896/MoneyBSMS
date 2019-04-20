from django.shortcuts import render
from django.http import HttpResponse
from .models import Wallet, Category, Transaction, Category_tranlation, Language
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from datetime import date, datetime
dstr = datetime.today().strftime('%Y-%m-%d')
ddate = datetime.today()
from .sms import *

user_language = 'English'
category_tranlation = Category_tranlation.objects.filter(language__name=user_language)

from django.utils import translation
cur_language = translation.get_language()

def switch_language(request):
    global cur_language
    global user_language
    global category_tranlation
    if cur_language == 'en' or cur_language == 'en-us':
        user_language = 'Việt Nam'
        cur_language = 'vi'
        category_tranlation = Category_tranlation.objects.filter(language__name=user_language)
    elif cur_language == 'vi':
        user_language = 'English'
        category_tranlation = Category_tranlation.objects.filter(language__name=user_language)
        cur_language = 'en'
    translation.activate(cur_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = cur_language
    return redirect('money:base_generic')

def base_generic(request):
    if request.user.is_authenticated:
        return redirect('money:transactions')
    else:
        context = {
            'language': user_language,
        }
        return render(request, 'base_generic.html', context)

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
        return render(request, 'registration/register.html')

import calendar
def decrement_month(request):
    global ddate
    month = ddate.month - 1 - 1
    year = ddate.year + month // 12
    month = month % 12 + 1
    day = min(ddate.day, calendar.monthrange(year,month)[1])
    ddate = datetime(year, month, day)
    return redirect('money:transactions')

def increment_month(request):
    global ddate
    month = ddate.month - 1 + 1
    year = ddate.year + month // 12
    month = month % 12 + 1
    day = min(ddate.day, calendar.monthrange(year,month)[1])
    ddate = datetime(year, month, day)
    return redirect('money:transactions')

def dec_month(request, wallet_id):
    global ddate
    month = ddate.month - 1 - 1
    year = ddate.year + month // 12
    month = month % 12 + 1
    day = min(ddate.day, calendar.monthrange(year,month)[1])
    ddate = datetime(year, month, day)
    return redirect('money:transactions_in_wallet', wallet_id)

def inc_month(request, wallet_id):
    global ddate
    month = ddate.month - 1 + 1
    year = ddate.year + month // 12
    month = month % 12 + 1
    day = min(ddate.day, calendar.monthrange(year,month)[1])
    ddate = datetime(year, month, day)
    return redirect('money:transactions_in_wallet', wallet_id)
    
#from django.core.exceptions import ObjectDoesNotExist

def transactions(request):#login_view all_wallets
    username = request.user.username
    all_wallets = Wallet.objects.filter(user=request.user.id)
    #Entry.objects.filter(blog__name='Beatles Blog')
    if len(all_wallets) != 0:
        all_transactions = Transaction.objects.filter(wallet__user__id=request.user.id).filter(time__month=ddate.month, time__year=ddate.year)
        class Wallets:
            inflow = '0'
            balance = '0'
            outflow = '0'
        wallet = Wallets()
        for tr in all_transactions:
            if tr.category.code == 'E':
                wallet.outflow = str(int(tr.amount) + int(wallet.outflow))
            elif tr.category.code == 'I':
                wallet.inflow = str(int(tr.amount) + int(wallet.inflow))
        wallet.balance = str(int(wallet.inflow) - int(wallet.outflow))
        context = {
            'username':username,
            'wallet': wallet,
            'all_transactions': all_transactions,
            'category': category_tranlation,
            'all_wallets': all_wallets,
            'in_wallet':'All wallets',
            'date': dstr,
            'bank': bank,
            'ddate': ddate.strftime('%B-%Y'),
            'cur_language': cur_language,
        }
        return render(request, 'money/transactions.html', context)
    else:
        context = {
            'username':username,
        }
        return render(request, 'money/wallet.html', context)
    
def transactions_in_wallet(request, wallet_id):
    username = request.user.username
    all_wallets = Wallet.objects.filter(user=request.user.id)
    w = Wallet.objects.get(pk=wallet_id)
    #Entry.objects.filter(blog__name='Beatles Blog')
    all_transactions = Transaction.objects.filter(wallet=wallet_id).filter(time__month=ddate.month, time__year=ddate.year)
    class Wallets:
            inflow = '0'
            balance = '0'
            outflow = '0'
            name = w.name
    wallet = Wallets()
    for tr in all_transactions:
        if tr.category.code == 'E':
            wallet.outflow = str(int(tr.amount) + int(wallet.outflow))
        elif tr.category.code == 'I':
            wallet.inflow = str(int(tr.amount) + int(wallet.inflow))
    wallet.balance = str(int(wallet.inflow) - int(wallet.outflow))
    context = {
        'username':username,
        'wallet': wallet,
        'all_transactions': all_transactions,
        'category': category_tranlation,
        'all_wallets': all_wallets,
        'in_wallet': wallet.name,
        'wallet_id': int(wallet_id),
        'date': dstr,
        'bank': bank,
        'ddate': ddate.strftime('%B-%Y'),
        'cur_language': cur_language,
    }
    return render(request, 'money/transactions.html', context)
    
def add_wallet(request):
    username = request.user.username
    name = request.POST['name']
    balance = request.POST['balance']
    #userId = request.user.username
    a = True
    all_wallets = Wallet.objects.filter(user=request.user.id)
    for wallet in all_wallets:
        if name == wallet.name:
            a = False
            break
    if a:
        w = Wallet(user=request.user, name=name, balance=balance)
        w.save()
        lcategory = Category.objects.filter(category_tranlation__name='Others_Income').get()
        t = Transaction(wallet = w, amount=balance, category=lcategory, time=dstr)
        t.save()
        return redirect('money:transactions_in_wallet', w.id)
    else:
        context = {
            'username':username,
        }
        return render(request,'money/wallet.html', context)
        
    
def add_transaction(request):
    amount = request.POST['amount']
    #lcategory = Category.objects.get(name=request.POST['category'])
    lcategory = Category.objects.get(category_tranlation__name=request.POST['category'])
    #wallet = Wallet.objects.filter(user=request.user).exclude(name=request.POST['wallet']).get()
    wallet = Wallet.objects.filter(name=request.POST['wallet']).get(user=request.user)
    #name=request.POST.get('category', False)
    #print(name)
    note = request.POST['note']
    time = request.POST['time']
    #userId = request.user.username
    t = Transaction(wallet = wallet, amount=amount, category=lcategory, note=note, time=time)
    #w.user_username=username
    #print(username)
    #print(w.User)
    t.save()
    wallet.save()
    return redirect('money:transactions_in_wallet', wallet.id)

def add_message(request):
    messag = request.POST.get('message', False)
    wallet = Wallet.objects.filter(name=request.POST['wallet']).get(user=request.user)
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
            
    if i >= 0:
        Message(message, i)
        lcategory = Category.objects.get(category_tranlation__name=result['Category'])
        t = Transaction(wallet = wallet, amount=result['Amount'], category=lcategory, note=result['Note'], time=result['Time'])
        t.save()
        wallet.save()
    return redirect('money:transactions_in_wallet', wallet.id)


def delete_or_edit(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    wallet = Wallet.objects.filter(transaction__id=transaction_id).get()
    if 'yes' in request.POST:
        wallet.save()
        transaction.delete()
        return redirect('money:transactions_in_wallet', wallet.id)
    elif 'save' in request.POST:
        transaction.amount = request.POST['amount']
        lcategory = Category.objects.get(category_tranlation__name=request.POST['category'])
        transaction.category = lcategory
        transaction.note = request.POST['note']
        transaction.time = request.POST['time']
            
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
        
        categ_amount= Transaction.objects.filter(wallet__user=request.user.id, category__code = 'E', time__month=ddate.month).values('category').order_by('category').annotate(total_amount=Sum('amount'))
        
        #categ_amount = Transaction.objects.values('category').order_by('category').annotate(total_amount=Sum('amount'))
        
        #print(request.user)
        #print(categ_amount)
        
        labels = []
        color = []
        default_items = []
        #fruits.append("orange")
        for c in categ_amount:
            cate = Category.objects.get(pk=c['category'])
            catetl = Category_tranlation.objects.get(category=cate, language__name=user_language)
            default_items.append(c['total_amount'])
            labels.append(catetl.name)
            color.append(cate.color)

        data = {
                "labels": labels,
                "default": default_items,
                "color": color,
        }
        return Response(data)
    
class ChartDataWallet(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, wallet_id, format=None):
        
        categ_amount= Transaction.objects.filter(wallet = wallet_id, category__code = 'E', time__month=ddate.month).values('category').order_by('category').annotate(total_amount=Sum('amount'))
        
        #categ_amount = Transaction.objects.values('category').order_by('category').annotate(total_amount=Sum('amount'))
        
        #print(request.user)
        #print(categ_amount)
        
        labels = []
        color = []
        default_items = []
        #fruits.append("orange")
        for c in categ_amount:
            cate = Category.objects.get(pk=c['category'])
            catetl = Category_tranlation.objects.get(category=cate, language__name=user_language)
            default_items.append(c['total_amount'])
            labels.append(catetl.name)
            color.append(cate.color)

        data = {
                "labels": labels,
                "default": default_items,
                "color": color,
        }
        return Response(data)





























