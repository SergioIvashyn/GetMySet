from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _('Technology')
        verbose_name_plural = _('Technologies')

    def __str__(self):
        return f'{self.pk}-{self.name}'
