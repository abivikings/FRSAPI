from django.contrib.auth.models import User
from django.db import models
from base.models import *


class Donations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    anonymous_location = models.TextField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
