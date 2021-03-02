from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProjectSet(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    notes = models.TextField()
    is_private = models.BooleanField(default=False)
    set = models.ForeignKey('UserSet', on_delete=models.CASCADE)
    is_original = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('ProjectSet')
        verbose_name_plural = _('ProjectSets')

    def __str__(self):
        return f'{self.id}-{self.name}'
