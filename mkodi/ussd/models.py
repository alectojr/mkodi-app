from django.db import models

class USSDSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    tin_number = models.CharField(max_length=20, blank=True, null=True)
    nida_number = models.CharField(max_length=20, blank=True, null=True)
    current_step = models.CharField(max_length=50, default='menu')
    temp_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.current_step}"
