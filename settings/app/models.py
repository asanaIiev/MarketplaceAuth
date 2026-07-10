from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

STATUS_CHOICES = [
    ('Client', 'Client'),
    ('Owner', 'Owner')
]

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    status = models.CharField(choices=STATUS_CHOICES, default='Client')
    registered_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} - {self.status}'