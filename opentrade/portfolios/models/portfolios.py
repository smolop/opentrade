import uuid
from django.db import models


class Portfolio(models.Model):

    ident = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False
        )

    value = models.FloatField(max_length=16, default=0.0)
    
