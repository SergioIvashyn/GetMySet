from django.db import models


# Create your models here.
from apps.project.models import Project
from apps.set.models import Set


class ProjectSet(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    notes = models.TextField()
    is_private = models.BooleanField(default=False)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    set_id = models.ForeignKey(Set, on_delete=models.CASCADE)
    is_original = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}-{self.name}'
