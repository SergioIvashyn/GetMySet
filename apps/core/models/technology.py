from django.db import models
from django.utils.translation import ugettext_lazy as _


class TechnologyManager(models.Manager):

    def project_page_qs(self, request):
        return self.get_queryset().filter(projects__user=request.user).distinct()


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = TechnologyManager()

    class Meta:
        verbose_name = _('Technology')
        verbose_name_plural = _('Technologies')

    def __str__(self):
        return f'{self.pk}-{self.name}'
