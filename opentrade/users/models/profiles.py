from django.db import models

from opentrade.utils.models import OpenTradeModel
from opentrade.portfolios.models import Portfolio
from opentrade.wallets.models import Wallet
from opentrade.users.models import User

from rest_framework.authtoken.models import Token

class Profile(OpenTradeModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created = models.DateField(auto_now_add=True)

    birthdate = models.DateField()

    currency_choice = [
        ('EUR', 'Euro'),
        ('USD', 'Dollar')
    ]

    currency = models.CharField(
        max_length=3,
        choices=currency_choice,
        default='EUR'
    )

    portfolio = models.OneToOneField(
        Portfolio,
        on_delete=models.CASCADE
    )

    wallet = models.OneToOneField(
        Wallet,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)