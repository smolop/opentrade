from django.db import models

from opentrade.users.models import User

import uuid

class AbstractAsset(models.Model):

    ref = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=4)
    date = models.DateField(auto_now=True)
    timestamp = models.TimeField(auto_now=True)
    quantity = models.IntegerField(blank=False, null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return ' {} : {} {}'.format( self.symbol, self.date, self.timestamp)

    def get_quantity(self):
        return self.quantity

class Favorite(models.Model):

    ref = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=4)
    user = models.ForeignKey(
                User,
                related_name='favorite_of',
                on_delete=models.CASCADE
            )

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
        ordering = ['-user', '-symbol']

    def __str__(self):
        return ' {} : {}'.format(self.user ,self.symbol)