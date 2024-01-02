from rest_framework import serializers
from donor.models import *


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'


class DonorCardSerializer(serializers.ModelSerializer):
    campaign = DonorSerializer()

    class Meta:
        model = CardInfo
        fields = '__all__'


class CampAdminDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignDetails
        fields = '__all__'
