from django.db import models
from django.utils.translation import ugettext_lazy as _
from demo import settings
from django.utils import timezone


def current_year() -> int:
    return timezone.now().year


class Company(models.Model):
    name = models.CharField(max_length=128, unique=True)
    year_founded = models.PositiveIntegerField(default=current_year)
    site_url = models.URLField()
    email = models.EmailField()
    slogan = models.TextField()
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos')
    company_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return f'{self.id}-{self.name}'
