from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from opentrade.users.permissions import IsAccountOwner

from opentrade.api.serializers.wallets import WalletModelSerializer
from opentrade.api.serializers.portfolios import PortfolioModelSerializer
from opentrade.api.serializers.profiles import ProfileModelSerializer
from opentrade.api.serializers.users import (
    AccountVerificationSerializer,
    UserSignInSerializer,
    UserModelSerializer,
    UserSignUpSerializer
)

from opentrade.users.models import User, Profile
from opentrade.portfolios.models import Portfolio
from opentrade.wallets.models import Wallet



class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.

    Handle sign up, signin and account verification.
    """

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'signin', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def signin(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation!, now you can improve your trading skills!'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update profile data."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)
    
    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        profile = Profile.objects.get(
            user=request.user
        )
        data = {
            'user': response.data,
            'portfolio': PortfolioModelSerializer(profile.portfolio).data,
            'wallet': WalletModelSerializer(profile.wallet).data
        }
        response.data = data
        return response


