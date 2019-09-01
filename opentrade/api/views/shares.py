from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from opentrade.users.permissions import IsAccountOwner

from opentrade.portfolios.models import Portfolio
from opentrade.users.models import Profile

from opentrade.assets.models import Favorite

from opentrade.assets.models import ScheduledSharesOperations

from opentrade.api.serializers.shares import (
    ShareModelSerializer,
    SharesCloseSerializer,
    SharesOperationSerializer,
    FavoriteModelSerializer,
    FavoriteFollowSerializer,
    FavoriteUnfollowSerializer,
    FavoriteIsFollowedSerializer,
    SharesScheduleOperationModelSerializer,
    SharesScheduleOperationSerializer,
    CancelSharesScheduleOperationSerializer,
    CloseSharesScheduleOperationSerializer
)
from opentrade.api.serializers.portfolios import PortfolioModelSerializer


from opentrade.utils.functions import shares as f_shares

import json

class ShareViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = PortfolioModelSerializer


    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['symbol', 'hystory']:
            permissions = [AllowAny]
        elif self.action in ['buy', 'sell', 'close']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def buy(self, request):
        return self.generic_operation(request, 'b')

    @action(detail=False, methods=['post'])
    def sell(self, request):
        return self.generic_operation(request, 's')
    
    @action(detail=False, methods=['post'])
    def close(self, request):
        profile = Profile.objects.get(user=request.user)
        print(request.data)
        serializer = SharesCloseSerializer(
            data=request.data, 
            context={'profile': profile}
            )
        serializer.is_valid(raise_exception=True)
        shares = serializer.save()
        data = ShareModelSerializer(shares).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def favorites(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        data = {'favorites': FavoriteModelSerializer(favorites, many=True).data}
        return Response(data)

    @action(detail=False, methods=['post'])
    def follow(self, request):
        user = request.user
        serializer = FavoriteFollowSerializer(
            data = request.data, 
            context = {'user': user}
            )
        serializer.is_valid(raise_exception=True)
        favorite = serializer.save()
        data = FavoriteModelSerializer(favorite).data
        return Response(data, status=status.HTTP_200_OK) 

    @action(detail=False, methods=['post'])
    def is_followed(self, request):
        user = request.user
        serializer = FavoriteIsFollowedSerializer(
            data = request.data, 
            context = {'user': user}
            )
        serializer.is_valid(raise_exception=True)
        is_followed = serializer.save()
        data = is_followed
        return Response(data, status=status.HTTP_200_OK) 

    @action(detail=False, methods=['post'])
    def unfollow(self, request):
        user = request.user
        serializer = FavoriteUnfollowSerializer(
            data = request.data, 
            context = {'user': user}
            )
        serializer.is_valid(raise_exception=True)
        favorite = serializer.save()
        data = FavoriteModelSerializer(favorite).data
        favorite.delete()
        return Response(data, status=status.HTTP_200_OK) 

    @action(detail=False, methods=['post'])
    def quotes(self, request):
        symbol = request.data['symbol']
        return Response(f_shares.get_quotes(symbol).json())

    @action(detail=False, methods=['post'])
    def price(self, request):
        symbol = request.data['symbol']
        return Response(f_shares.get_price(symbol))

    @action(detail=False, methods=['post'])
    def change_percentage(self, request):
        symbol = request.data['symbol']
        return Response(f_shares.get_chage_percentage(symbol))

    @action(detail=False, methods=['post'])
    def history(self, request):
        symbol = request.data['symbol']
        interval, start, end = None, None, None
        if 'interval' in request.data:
            interval = request.data['interval']
        if 'start' in request.data:
            start = request.data['start']
        if 'end' in request.data:
            end = request.data['end']
        data = f_shares.get_history(
            symbol, 
            interval, 
            start, 
            end
        ).json()
        return Response(data)

    @action(detail=False, methods=['post'])
    def schedule_share_operation(self, request):
        user = request.user
        serializer = SharesScheduleOperationSerializer(
            data = request.data,
            context = {'user': user}
        )
        serializer.is_valid(raise_exception=True)
        schedule_operation = serializer.save()
        data = SharesScheduleOperationModelSerializer(schedule_operation).data
        print(data)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def get_schedule_shares_operations(self, request):
        user=request.user
        schedule_shares_operations = ScheduledSharesOperations.objects.filter(user=user)
        data = {
            'shudele_shares_operations': SharesScheduleOperationModelSerializer(
                schedule_shares_operations, 
                many=True
                ).data
                }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def cancel_schedule_share_operation(self, request):
        user = request.user
        serializer = CancelSharesScheduleOperationSerializer(
            data = request.data,
            context = { 'user': user}
        )
        serializer.is_valid(raise_exception=True)
        schedule_operation = serializer.save()
        data = { 
            'schedule_operation': SharesScheduleOperationModelSerializer(schedule_operation).data 
            }
        schedule_operation.delete()
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def close_schedule_share_operation(self, request):
        user = request.user
        serializer = CloseSharesScheduleOperationSerializer(
            data = request.data,
            context = { 'user': user}
        )
        serializer.is_valid(raise_exception=True)
        schedule_operation = serializer.save()
        data = SharesScheduleOperationModelSerializer(schedule_operation).data 
        return Response(data, status=status.HTTP_201_CREATED)

    def generic_operation(self, request, op):
        profile = Profile.objects.get(user=request.user)
        serializer = SharesOperationSerializer(
            data=request.data, 
            context={'profile': profile, 'op': op}
            )
        serializer.is_valid(raise_exception=True)
        shares = serializer.save()
        data = ShareModelSerializer(shares).data
        return Response(data, status=status.HTTP_201_CREATED)