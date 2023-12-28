from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from donor.models import *
from . serializers import *


class DonorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
