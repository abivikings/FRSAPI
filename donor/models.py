from django.contrib.auth.models import User
from django.db import models
from base.models import *


class Donor(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.TextField(max_length=50, null=True)
    last_name = models.TextField(max_length=50, null=True)
    email = models.EmailField(max_length=50, null=True)


class CardInfo(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    card_number = models.TextField(max_length=100, null=True)
    card_exp_date = models.TextField(max_length=100, null=True)
    wallet_address = models.TextField(max_length=100, null=True)
