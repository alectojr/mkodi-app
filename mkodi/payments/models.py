from django.db import models
from taxpayers.models import Taxpayer

class Payment(models.Model):
    taxpayer = models.ForeignKey(Taxpayer, on_delete=models.CASCADE)
    control_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # pending, completed, failed
    payment_method = models.CharField(max_length=50, default='mobile_money')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.taxpayer} - {self.control_number} ({self.status})"