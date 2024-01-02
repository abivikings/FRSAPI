from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from donor.models import *
from . serializers import *
from rest_framework.decorators import api_view, permission_classes


class DonorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


class CampAdminDashboardViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CampaignDetails.objects.all()

    serializer_class = CampAdminDashboardSerializer

