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
    
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def logged_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('money:transactions')
    else:
        return render(request, 'registration/login.html')

from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

category = Category.objects.all()
def transactions(request):#login_view
    try:
        username = request.user.username
        wallet = Wallet.objects.get(user=request.user.id)
        #Entry.objects.filter(blog__name='Beatles Blog')
        all_transactions = Transaction.objects.filter(wallet=wallet.id)
        context = {
            'username':username,
            'wallet': wallet,
            'all_transactions': all_transactions,
            'category': category,
        }
        return render(request, 'money/transactions.html', context)
    except (ObjectDoesNotExist):
        context = {
            'username':username,
        }
        return render(request, 'money/wallet.html', context)

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
    return redirect('money:transactions')
    
def add_transaction(request):
    amount = request.POST['amount']
    lcategory = Category.objects.get( name=request.POST['category'])
    #name=request.POST.get('category', False)
    #print(name)
    note = request.POST['note']
    time = request.POST['time']
    #userId = request.user.username
    wallet = Wallet.objects.get(user=request.user.id)
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
    return redirect('money:transactions')
    
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'registration/logged_out.html')



































