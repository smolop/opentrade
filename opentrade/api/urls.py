from django.urls import include, path

from rest_framework.routers import DefaultRouter

from opentrade.api.views import users as user_views
from opentrade.api.views import shares as share_views
from opentrade.api.views import portfolios as portfolio_views
from opentrade.api.views import wallets as wallet_views

router = DefaultRouter()

router.register(r'users', user_views.UserViewSet, basename='users')
router.register(r'shares', share_views.ShareViewSet, basename='shares')
router.register(r'portfolio', portfolio_views.PortfolioViewSet, basename='portfolio')
router.register(r'wallet', wallet_views.WalletViewSet, basename='wallet')

urlpatterns = [
    
    path('', include(router.urls)),

]

