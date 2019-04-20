from django.contrib import admin
from .models import Wallet, Category, Transaction, Category_tranlation, Language
# Register your models here.

admin.site.register(Wallet)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Category_tranlation)
admin.site.register(Language)
