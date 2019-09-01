from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from opentrade.users.permissions import IsAccountOwner

from opentrade.api.serializers.wallets import WalletModelSerializer

from opentrade.users.models import Profile
from opentrade.wallets.models import Wallet

class WalletViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = WalletModelSerializer

    def get_queryset(self):
        """Restrict list to public-only."""
        user = self.user
        profile = Profile.objects.get(user=user)
        queryset = Wallet.objects.filter(portfolio=portfolio)
        return queryset

    def get_permissions(self):
        permissions = [IsAuthenticated, IsAccountOwner]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def amount(self, request):
        profile = Profile.objects.get(user=request.user)
        data = {'wallet': WalletModelSerializer(profile.wallet).data}
        return Response(data)