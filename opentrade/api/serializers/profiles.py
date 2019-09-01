from rest_framework import serializers

from opentrade.users.models import Profile, User


class ProfileModelSerializer(serializers.ModelSerializer):


    class Meta:
    
        model = Profile
        # fields = '__all__'
        fields = (
            'birthdate',
            'currency'
        )

        