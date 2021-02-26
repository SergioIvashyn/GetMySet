from django.db import models

# Create your models here.


class IndustryManager(models.Manager):
    pass


class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = IndustryManager()

    def __str__(self):
        return f'{self.id}-{self.name}'
