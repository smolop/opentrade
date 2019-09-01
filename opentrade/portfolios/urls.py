from django.urls import path

from opentrade.portfolios import views

urlpatterns = [
    
    path(
        route='portfolio/',
        view=views.portfolio,
        name='portfolio'
    ),

    path(
        route='summary/',
        view=views.summary,
        name='summary'
    ),

]