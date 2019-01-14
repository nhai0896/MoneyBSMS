from django.shortcuts import render
from django.http import HttpResponse
from .models import Wallet, Category, Transaction
from django.contrib.auth.models import User

def base_generic(request):
    #return 0 cac ham lien ket trong url phai tra ve httpresponse 
    return render(request, 'base_generic.html')
def register(request):
    return render(request, 'registration/register.html')

from django.db import IntegrityError
import logging
logger = logging.getLogger(__name__)

def create_account(request):
    username = request.POST['username']#neu dung id cua label thi: request.POST.get('usernemr', False)
    password = request.POST['password']
    try:
        user = User.objects.create_user(username=username, password=password)
        message = 'successfully!'
        logger.info(message)
        return render(request, 'registration/login.html')
    except (IntegrityError): 
        message = 'account existed!'
        logger.info(message)
        return render(request, 'registration/login.html')

from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
#inflow, outflow, balance 

category = Category.objects.all()

@login_required
def transactions(request):
    try:
        userId = request.user.id
        #wallet = Wallet.objects.get(user=userId) //loi vi 1 user co the co nhieu hon 1 wallet
        wallets = Wallet.objects.filter(user__id = userId)
            #Entry.objects.filter(blog__name='Beatles Blog')
            #all_transactions = Transaction.objects.filter(wallet=wallet.id) chua test
        #all_transactions = Transaction.objects.filter(wallet__id=wallet.id)
        all_transactions = Transaction.objects.all()
        context = {
            #'wallet': wallet,
            'username':request.user.username,
            'wallets': wallets,
            'all_transactions': all_transactions,
            'category': category,
        }
        return render(request, 'money/transactions.html', context)
    except (ObjectDoesNotExist):
        return render(request, 'money/wallet.html')
    
def add_wallet(request):
    name = request.POST['name']
    currency = request.POST['currency']
    balance = request.POST['balance']
    #userId = request.user.username
    w = Wallet(user=request.user, name=name, currency=currency, balance=balance)
    #w.user_username=username
    #print(username)
    #print(w.User)
    w.save()
    all_transactions = Transaction.objects.filter(wallet__id=w.id)
    category = Category.objects.get( name=request.POST['category'])
    context = {
        'all_transactions': all_transactions,
        'category': category
    }
    return render(request, 'money/transactions.html', context)

def add_transaction(request):
    amount = request.POST['amount']
    category = Category.objects.get( name=request.POST['category'])
    #name=request.POST.get('category', False)
    #print(name)
    note = request.POST['note']
    time = request.POST['time']
    #userId = request.user.username
    wallet = Wallet.objects.get(id=request.POST['wallet'])
    t = Transaction(wallet = wallet, amount=amount, category=category, note=note, time=time)
    #w.user_username=username
    #print(username)
    #print(w.User)
    t.save()
    all_transactions = Transaction.objects.filter(wallet__id=wallet.id)
    context = {
        'all_transactions': all_transactions,
    }
    return render(request, 'money/transactions.html', context)

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'registration/logged_out.html')



































