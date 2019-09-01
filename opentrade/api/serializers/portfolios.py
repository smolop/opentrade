from rest_framework import serializers
from opentrade.portfolios.models import Portfolio


class PortfolioModelSerializer(serializers.Serializer):

    value = serializers.FloatField(max_value=9999999999.999999)