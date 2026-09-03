from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	photo = models.FileField(upload_to='profile_photos/', blank=True, null=True)

	def __str__(self):
		return f"Profile for {self.user.username}"
