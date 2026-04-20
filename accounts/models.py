from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    company_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    headline = models.CharField(max_length=255, blank=True)
    rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    portfolio = models.URLField(blank=True)
    availability = models.CharField(max_length=100, blank=True)
    skills = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username