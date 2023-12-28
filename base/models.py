from django.contrib.auth.models import User
from django.db import models


class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_approved = models.BooleanField(null=True, default=False)
    is_active = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.name, self.is_approved


class CampaignDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    collected_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Details for {self.campaign.name}"
