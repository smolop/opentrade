from django.urls import include, path

from rest_framework.routers import DefaultRouter

from opentrade.utils import views


urlpatterns = [
    
    path(
        route='line_chart_json/<str:symbol>',
        view=views.LineChartJSONView.as_view(),
        name='line_chart_json'
    )

]