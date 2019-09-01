import uuid
from django.db import models


class Wallet(models.Model):

    ident = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False
        )
    init_amount = models.FloatField(default=40000.0)
    amount = models.FloatField(default=40000.0)
