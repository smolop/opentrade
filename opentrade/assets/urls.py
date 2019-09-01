from django.urls import path

from opentrade.assets import views

urlpatterns = [

    path(
        route='dev_mode/',
        view=views.dev_mode_view,
        name='dev_mode'
    ),

    path(
        route='favorites/',
        view=views.favorites_view,
        name='favorites'
    ),

    path(
        route='schedule_operations/',
        view=views.schedule_ops_view,
        name='schedule_operations'
    ),

    path(
        route='help/',
        view=views.help_view,
        name='help'
    ),

    path(
        route='share/<str:symbol>',
        view=views.share_view,
        name='share_detail'
    ),

]