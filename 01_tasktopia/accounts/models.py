from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text='Optional. Enter your phone number.'
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text='Optional. Enter your location.'
    )

    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'
    
    def __str__(self):
        return self.user.username
