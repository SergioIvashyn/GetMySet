from django.db import models

# Create your models here.
from apps.industry.models import Industry
from apps.technology.models import Technology


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    notes = models.CharField(max_length=30)
    is_private = models.BooleanField(default=False)
    technologies = models.ManyToManyField(Technology, blank=True, related_name='technologies')
    industries = models.ManyToManyField(Industry, blank=True, related_name='industries')

    def __str__(self):
        return f'{self.pk}-{self.name}'
