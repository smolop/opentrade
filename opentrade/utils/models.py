from django.db import models


class OpenTradeModel(models.Model):

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time about when was created the object.'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time about when was the last modify of the object.'
    )

    class Meta:
        """Meta option."""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']
