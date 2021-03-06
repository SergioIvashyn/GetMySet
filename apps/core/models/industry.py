from django.db import models
from django.utils.translation import ugettext_lazy as _


class IndustryManager(models.Manager):

    def project_page_qs(self, request):
        return self.get_queryset().filter(projects__user=request.user).distinct()


class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = IndustryManager()

    class Meta:
        verbose_name = _('Industry')
        verbose_name_plural = _('Industries')

    def __str__(self):
        return f'{self.id}-{self.name}'
