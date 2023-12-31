from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'campaign-details', CampaignDetailsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('call_stored_procedure/', CallStoredProcedure, name='call_stored_procedure'),
    path('create_user/', create_user, name='create_user'),
    path('login/', login, name='login'),
    path('auth_me/', auth_me, name='auth_me'),
    path('get_auth_group/', get_auth_group, name='get_auth_group'),
]
