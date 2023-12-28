from django.urls import path, include
from rest_framework.routers import DefaultRouter

from camp_admin.views import *


router = DefaultRouter()
router.register(r'donor', DonorViewSet)


urlpatterns = [
    path('', include(router.urls))
]
