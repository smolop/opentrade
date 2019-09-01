from rest_framework import serializers
from opentrade.wallets.models import Wallet

class WalletModelSerializer(serializers.ModelSerializer):

    class Meta:

        model=Wallet
        fields=(
            'init_amount',
            'amount'
        )
    