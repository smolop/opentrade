"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

# To get_token_user
from django.conf.urls import url
from rest_framework.authtoken import views as rest_framework_views

#import ipdb; ipdb.set_trace()

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/', include(('opentrade.api.urls', 'api'), namespace='api')),
    path('users/', include(('opentrade.users.urls', 'users'), namespace='users')),
    path('portfolios/', include(('opentrade.portfolios.urls', 'portfolios'), namespace='portfolios')),
    path('assets/', include(('opentrade.assets.urls', 'assets'), namespace='assets')),
    path('utils/', include(('opentrade.utils.urls', 'utils'), namespace='utils')),
    #url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
