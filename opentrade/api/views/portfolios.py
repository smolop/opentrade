from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from opentrade.users.permissions import IsAccountOwner

from opentrade.portfolios.models import Portfolio
from opentrade.users.models import Profile
from opentrade.assets.models import Share

from opentrade.api.serializers.portfolios import PortfolioModelSerializer
from opentrade.api.serializers.shares import ShareModelSerializer

from opentrade.utils.functions import shares as f_shares

class PortfolioViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = PortfolioModelSerializer

    def get_queryset(self):
        """Restrict list to public-only."""
        user = self.user
        profile = Profile.objects.get(user=user)
        queryset = Share.objects.filter(portfolio=portfolio)
        return queryset

    def get_permissions(self):
        permissions = [IsAuthenticated, IsAccountOwner]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def summary(self, request):
        profile = Profile.objects.get(user=request.user)
        shares = Share.objects.filter(portfolio=profile.portfolio)
        data = {'shares': ShareModelSerializer(shares, many=True).data}
        return Response(data)

    @action(detail=False, methods=['post'])
    def all(self, request):
        profile = Profile.objects.get(user=request.user)
        shares = Share.objects.filter(portfolio=profile.portfolio, closed=False)
        data = {'shares': ShareModelSerializer(shares, many=True).data}
        print(data)
        return Response(data)

    @action(detail=False, methods=['post'])
    def buyings(self, request):
        profile = Profile.objects.get(user=request.user)
        return self.get_shares(profile.portfolio, 'b')
    
    @action(detail=False, methods=['post'])
    def sellings(self, request):
        profile = Profile.objects.get(user=request.user)
        return self.get_shares(profile.portfolio, 's')

    @action(detail=False, methods=['post'])
    def value(self, request):
        profile = Profile.objects.get(user=request.user)
        shares = Share.objects.filter(portfolio=profile.portfolio, closed=False)
        val = 0
        for s in shares:
            val += (s.quantity * f_shares.get_price(s.symbol))
        data = {'value': val}
        return Response(data)
    
    def get_shares(self, portfolio, op):
        shares = Share.objects.filter(portfolio=portfolio, operation=op, closed=False)
        data = {'shares': ShareModelSerializer(shares, many=True).data}
        return Response(data)

