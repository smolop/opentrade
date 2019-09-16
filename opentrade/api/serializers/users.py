from django.conf import settings
from django.contrib.auth import password_validation, authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from opentrade.users.models import User, Profile
from opentrade.portfolios.models import Portfolio
from opentrade.wallets.models import Wallet

from opentrade.taskapp.tasks import send_confirmation_email, gen_verification_token

from opentrade.api.serializers.profiles import ProfileModelSerializer

import jwt

class UserModelSerializer(serializers.ModelSerializer):

    profile = ProfileModelSerializer(read_only=True)

    class Meta:

        model = User
        fields = (
            'username',
            'email',
            'profile'
        )

class UserSignUpSerializer(serializers.Serializer):

    username = serializers.CharField(
        min_length=2,
        max_length=16,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    birthdate = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'])

    currency = serializers.CharField(
        min_length=3,
        max_length=3,
        default='EUR'
    )

    password = serializers.CharField(min_length=8, max_length=128)
    password_confirmation = serializers.CharField(min_length=8, max_length=128)

    def validate(self, data):
        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(password)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        birthdate = data.pop('birthdate')
        currency = data.pop('currency')
        user = User.objects.create_user(**data, is_verified=True)
        portfolio = Portfolio.objects.create()
        wallet = Wallet.objects.create()
        Profile.objects.create(
            user=user,
            birthdate=birthdate,
            currency=currency,
            portfolio=portfolio,
            wallet=wallet
        )
        send_confirmation_email(user_pk=user.pk)
        return user


class UserSignInSerializer(serializers.Serializer):

    username = serializers.CharField(min_length=2, max_length=16)
    #email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=128)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        user = self.context['user']
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class AccountVerificationSerializer(serializers.Serializer):

    token = serializers.CharField()

    def validate_token(self, data):

        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
