from rest_framework import serializers

from opentrade.assets.models import Share, Favorite, ScheduledSharesOperations
from opentrade.users.models import Profile, User
from opentrade.api.serializers.users import UserModelSerializer

from opentrade.utils.functions import (
    shares as f_shares,
    profile as f_profile
    )

from django.utils import timezone


class ShareModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Share
        #fields = '__all__'
        exclude = ('portfolio', )

class FavoriteModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Favorite
        fields = '__all__'

class SharesScheduleOperationModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = ScheduledSharesOperations

        fields = '__all__'
        #exclude = ('user', )

class FavoriteFollowSerializer(serializers.Serializer):

    symbol = serializers.CharField(max_length=4)

    def validate(self, data):
        user = self.context['user']
        if not f_shares.exists(data['symbol']):
            raise serializers.ValidationError("Symbol doesn't exists")
        return data

    def create(self, data):
        user = self.context['user']
        if not Favorite.objects.filter(symbol=data['symbol'], user=user).exists():
            favorite = Favorite.objects.create(symbol=data['symbol'], user=user)
            favorite.save()
        else:
            favorite = Favorite.objects.get(symbol=data['symbol'], user=user)
        return favorite

class FavoriteUnfollowSerializer(serializers.Serializer):

    symbol = serializers.CharField(max_length=4)

    def validate(self, data):
        user = self.context['user']
        if not f_shares.exists(data['symbol']):
            raise serializers.ValidationError("Symbol doesn't exists")
        if not Favorite.objects.filter(symbol=data['symbol'], user=user).exists():
            raise serializers.ValidationError("You don't have this  symbol in your favorites")
        return data

    def create(self, data):
        user = self.context['user']
        favorite = Favorite.objects.get(symbol=data['symbol'], user=user)
        return favorite

class FavoriteIsFollowedSerializer(serializers.Serializer):

    symbol = serializers.CharField(max_length=4)

    def validate(self, data):
        user = self.context['user']
        if not f_shares.exists(data['symbol']):
            raise serializers.ValidationError("Symbol doesn't exists")
        return data

    def create(self, data):
        user = self.context['user']
        if Favorite.objects.filter(symbol=data['symbol'], user=user).exists():
           return True
        return False


class SharesCloseSerializer(serializers.Serializer):

    ref = serializers.IntegerField(min_value=1)

    def validate(self, data):
        profile = self.context['profile']
        if not Share.objects.get(ref=data['ref'], portfolio=profile.portfolio):
            raise serializers.ValidationError("Share doesn't exists")
        shares = Share.objects.get(ref=data['ref'], portfolio=profile.portfolio)
        if shares.closed:
            raise serializers.ValidationError("Invalid operation")
        return data

    def create(self, data):
        profile = self.context['profile']
        shares = Share.objects.get(ref=data['ref'], portfolio=profile.portfolio)
        shares.closed=True
        amount = shares.quantity * f_shares.get_price(shares.symbol)
        f_profile.close_operation(profile, amount)
        f_profile.save(profile)
        shares.save()
        return shares



class SharesOperationSerializer(serializers.Serializer):

    symbol = serializers.CharField(max_length=4)
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        profile = self.context['profile']
        symbol = data['symbol']
        if not f_shares.exists(symbol):
            raise serializers.ValidationError("Symbol doesn't exist")
        amount = data['quantity'] * f_shares.get_price(symbol)
        if not f_profile.has_funds(profile, amount):
            raise serializers.ValidationError("Your funds aren't enough as required")
        return data

    def create(self, data):
        profile = self.context['profile']
        symbol = data['symbol']
        quant = data['quantity']
        op = self.context['op']
        price = f_shares.get_price(symbol)
        amount = quant * price
        f_profile.payoff_balance(profile, amount)
        shares = Share.objects.create(
            symbol = symbol,
            quantity = quant,
            price = price,
            operation = op,
            portfolio = profile.portfolio
        )
        f_profile.save(profile)

        return shares

class CancelSharesScheduleOperationSerializer(serializers.Serializer):

    ref = serializers.IntegerField(min_value=0)

    def validate(self, data):
        user = self.context['user']
        ref = data['ref']
        sch_op = ScheduledSharesOperations.objects.filter(ref=ref)
        if not sch_op:
            raise serializers.ValidationError("Schedule operation doesn't exist")
        return data

    def create(self, data):
        user = self.context['user']
        ref = data['ref']
        schedule_op = ScheduledSharesOperations.objects.get(ref=ref)
        return schedule_op

class CloseSharesScheduleOperationSerializer(serializers.Serializer):

    ref = serializers.IntegerField(min_value=0)
    min_price = serializers.FloatField()
    max_price = serializers.FloatField()
    schedule_start = serializers.DateTimeField()

    def validate(self, data):
        user = self.context['user']
        ref = data['ref']
        shares_order = Share.objects.filter(ref=ref, closed=False)
        if not shares_order:
            raise serializers.ValidationError("Shares oreder operation impossible to do!")
        return data

    def create(self, data):
        user = self.context['user']
        ref = data['ref']
        shares_order = Share.objects.get(ref=ref, closed=False)
        schedule_op = ScheduledSharesOperations.objects.create(
                user=user,
                symbol=shares_order.symbol,
                min_price=data['min_price'],
                max_price=data['max_price'],
                schedule_start=data['schedule_start'],
                operation='c',
                share_reference=shares_order
            )
        return schedule_op


class SharesScheduleOperationSerializer(serializers.ModelSerializer):

    class Meta:

        model = ScheduledSharesOperations

        #fields = '__all__'
        exclude = ('user', )

    def validate(self, data):
        user = self.context['user']
        symbol = data['symbol']
        schedule_start = data['schedule_start']
        operation = data['operation']
        if not f_shares.exists(symbol):
            raise serializers.ValidationError("Symbol doesn't exist")
        amount = data['quantity'] * f_shares.get_price(symbol)
        profile = Profile.objects.get(user=user)
        if not f_profile.has_funds(profile, amount):
            raise serializers.ValidationError("Your funds aren't enough as required")
        if schedule_start <= timezone.localtime():
            raise serializers.ValidationError("Schedule start invalid")
        if data['min_price'] < 0:
            raise serializers.ValidationError("Minimun price lesss than zero, seriously?")
        if data['max_price'] > 9999999999:
            raise serializers.ValidationError("Maximun price problem")
        return data

    def create(self, data):
        user = self.context['user']
        print(user)
        user_id = User.objects.get(username=user)
        schedule_operation = ScheduledSharesOperations.objects.create(**data, user=user_id)
        schedule_operation.save()
        return schedule_operation
