from django.db import models
from taxpayers.models import Taxpayer
from django.db import models
from taxpayers.models import Taxpayer

class LandRecord(models.Model):
    taxpayer = models.ForeignKey(Taxpayer, on_delete=models.CASCADE, related_name='land_records')
    parcel_number = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=255)
    size_acres = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ownership_type = models.CharField(max_length=100, default="Freehold")
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.parcel_number} - {self.location}"

class BrelaRecord(models.Model):
    taxpayer = models.OneToOneField(Taxpayer, on_delete=models.CASCADE)
    brela_number = models.CharField(max_length=50, unique=True)
    business_name = models.CharField(max_length=255)
    registration_date = models.DateField()
    business_type = models.CharField(max_length=100)
    assets_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    number_of_assets = models.IntegerField(default=0)
    last_filed = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.business_name} ({self.brela_number})"