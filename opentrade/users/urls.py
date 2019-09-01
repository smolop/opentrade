from django.urls import path

from opentrade.users import views

urlpatterns = [
    
    path(
        route='login/',
        view=views.login_view,
        name='login'
    ),
    path(
        route='register/',
        view=views.register_view,
        name='register'
    ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        route='home/',
        view=views.index,
        name='home'
    ),

     path(
        route='verify/',
        view=views.verify_view,
        name='verify'
    ),
    path(
        route='change_passwd/',
        view=views.change_pass_view,
        name='change_passwd'
    ),

]