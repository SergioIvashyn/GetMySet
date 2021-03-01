from django.db import models

# Create your models here.
from django.db.models import Manager

from apps.industry.models import Industry
from apps.technology.models import Technology
from demo import settings


class ProjectManager(Manager):
    def public(self):
        return self.get_queryset().filter(is_private=False).prefetch_related(
            'technologies').prefetch_related('industries')

    def private(self):
        return self.get_queryset().filter(is_private=True).prefetch_related(
            'technologies').prefetch_related('industries')


class Project(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    notes = models.CharField(max_length=30)
    is_private = models.BooleanField(default=False)
    technologies = models.ManyToManyField(Technology, blank=True, related_name='technologies')
    industries = models.ManyToManyField(Industry, blank=True, related_name='industries')

    objects = ProjectManager()

    class Meta:
        ordering = ['id']

    @property
    def is_url_working(self):
        return not bool(self.notes)

    def __str__(self):
        return f'{self.pk}-{self.name}'
