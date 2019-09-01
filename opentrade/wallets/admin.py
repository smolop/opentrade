from django.contrib import admin

# Register your models here.
from opentrade.wallets.models import Wallet

admin.site.register(Wallet)
