from django.contrib import admin

from opentrade.assets.models import Share, Option, Favorite, ScheduledSharesOperations


admin.site.register(Share)
#admin.site.register(Option)
@admin.register(Favorite)
class CustomFavorite(admin.ModelAdmin):
    """Favorite model."""

    list_display = ('user', 'symbol')
    list_filter = ('user', 'symbol')


@admin.register(ScheduledSharesOperations)
class CustomScheduledSharesOperations(admin.ModelAdmin):

    list_display = ('user', 'schedule_start', 'symbol', 'date', 'timestamp')
    list_filter = ('user', 'schedule_start')
    ordering = ('-user', 'schedule_start', '-symbol', '-date', '-timestamp')