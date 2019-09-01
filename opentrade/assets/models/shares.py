from .assets import *

from opentrade.portfolios.models import Portfolio

class Share(AbstractAsset):

    price = models.FloatField()

    operation_choice = [
        ('b', 'buy'),
        ('s', 'sell')
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
        related_name='shares_portfolio',
        on_delete=models.CASCADE
    )
    

    def __str__(self):
        return 'ref:{} [{}] {} : {} {} : {}'.format( 
                self.ref,
                self.operation, 
                self.symbol, 
                self.date, 
                self.timestamp, 
                self.closed
            )


class ScheduledSharesOperations(AbstractAsset):
    
    schedule_start = models.DateTimeField()
    
    max_price = models.FloatField()

    min_price = models.FloatField()

    operation_choice = [
        ('b', 'buy'),
        ('s', 'sell'),
    ]

    operation = models.CharField(
        max_length=1,
        choices=operation_choice,
        null=False,
        blank=False
    )

    user = models.ForeignKey(
                User,
                related_name='owner',
                on_delete=models.CASCADE
            )

    class Meta:
        verbose_name = 'scheduled_shares_operation'
        verbose_name_plural = 'scheduled_shares_operations'
        ordering = ['-user', 'schedule_start', '-symbol', '-date', '-timestamp']

    def __str__(self):
        return ' {} : {} schdule start: {}'.format(self.user ,self.symbol, self.schedule_start)