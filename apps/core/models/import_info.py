from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ImportInfo(models.Model):
    FAILED = 'failed'
    SUCCESS = 'success'
    PENDING = 'pending'
    PENDING_MESSAGE = f'{PENDING.title()} for uploading projects'
    STATUS_CHOICE = (
        (FAILED, _('Failed')),
        (SUCCESS, _('Success')),
        (PENDING, _('Pending')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICE, default=PENDING)
    message = models.TextField(blank=True, default=PENDING_MESSAGE)

    def __str__(self):
        return f'{self.user_id}-{self.status}'
