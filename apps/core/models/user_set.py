from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserSet(models.Model):
    name = models.CharField(max_length=200, unique=True)
    set_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('UserSet')
        verbose_name_plural = _('UserSets')

    def __str__(self):
        return f'{self.id}-{self.name}'
