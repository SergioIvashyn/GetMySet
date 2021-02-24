from django.db import models

# Create your models here.
from django.utils import timezone

from demo import settings


class Company(models.Model):
    name = models.CharField(max_length=128, unique=True)
    year_founded = models.PositiveIntegerField(default=timezone.now().year)
    site_url = models.URLField()
    email = models.EmailField()
    slogan = models.TextField()
    description = models.TextField(blank=True)
    logo = models.ImageField(storage='logos')
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.id}-{self.name}'
