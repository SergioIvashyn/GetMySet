from django.db import models

# Create your models here.
from demo import settings


class Set(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}-{self.name}'
