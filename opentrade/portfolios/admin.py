from django.contrib import admin

# Register your models here.
from opentrade.portfolios.models import Portfolio


admin.site.register(Portfolio)