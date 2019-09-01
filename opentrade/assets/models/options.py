from .assets import *

from opentrade.portfolios.models import Portfolio

class Option(AbstractAsset):

    price = models.FloatField()

    expiration = models.DateField()

    operation_choice = [
        ('c', 'call'),
        ('p', 'put')
    ]

    operation = models.CharField(
        max_length=1,
        choices=operation_choice,
        null=False,
        blank=False
    )

    closed = models.BooleanField(default=False)

    portfolio = models.ForeignKey(
        Portfolio,
        related_name='options_portofolio',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '[{}] {} : {} {} : {}'.format( 
                self.operation, 
                self.symbol, 
                self.date, 
                self.timestamp, 
                self.closed
            )