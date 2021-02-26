from django.db import models

# Create your models here.
from apps.industry.models import Industry
from apps.technology.models import Technology
from demo import settings


class Project(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    notes = models.CharField(max_length=30, blank=True)
    is_private = models.BooleanField(default=False)
    technologies = models.ManyToManyField(Technology, blank=True, related_name='technologies')
    industries = models.ManyToManyField(Industry, blank=True, related_name='industries')

    class Meta:

        unique_together = ('name', 'user_id')

    def __str__(self):
        return f'{self.pk}-{self.name}'
