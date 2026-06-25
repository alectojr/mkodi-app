from django.db import models

class Taxpayer(models.Model):
    nida_number = models.CharField(max_length=20, primary_key=True, unique=True)
    tin_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

    business_name = models.CharField(max_length=255, blank=True, null=True)
    brela_number = models.CharField(max_length=100, blank=True, null=True)
    land_parcel = models.CharField(max_length=100, blank=True, null=True)

    estimated_income = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tax_compliance_score = models.IntegerField(default=65)
    credit_score = models.IntegerField(default=60)

    is_active = models.BooleanField(default=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.tin_number or self.nida_number})"

