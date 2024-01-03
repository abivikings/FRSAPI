from django.urls import path, include
from .views import *

urlpatterns = [
    path('donate_by_stored_info/', DonateByStoredInfo, name='donate_by_stored_info'),
    path('save_card_info/', SaveCardInfo, name='save_card_info'),
    path('donate/', Donation, name='donate'),
]
