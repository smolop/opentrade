from django.urls import include, path

from rest_framework.routers import DefaultRouter

from opentrade.wallets.views import wallets as wallets_views

router = DefaultRouter()

router.register(r'wallets', wallets_views.WalletViewSet, basename='wallets')

urlpatterns = [
    path('', include(router.urls))
] 
