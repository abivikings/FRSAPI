from rest_framework import serializers
from .models import Campaign, CampaignDetails


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignDetailsSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer()

    class Meta:
        model = CampaignDetails
        fields = (
            'id', 'user', 'campaign', 'title', 'start_date', 'end_date', 'description', 'target_amount',
            'collected_amount')
