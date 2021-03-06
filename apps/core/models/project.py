from django.conf import settings
from django.db import models
from django.db.models import Manager
from django.utils.translation import ugettext_lazy as _

from apps.core.models.industry import Industry
from apps.core.models.technology import Technology


class ProjectManager(Manager):
    def public(self, request):
        return self.get_queryset().filter(is_private=False, user=request.user).prefetch_related(
            'technologies').prefetch_related('industries')

    def private(self, request):
        return self.get_queryset().filter(is_private=True, user=request.user).prefetch_related(
            'technologies').prefetch_related('industries')


class Project(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    notes = models.CharField(max_length=30, blank=True)
    is_private = models.BooleanField(default=False)
    technologies = models.ManyToManyField('Technology', blank=True, related_name='projects')
    industries = models.ManyToManyField('Industry', blank=True, related_name='projects')

    objects = ProjectManager()

    class Meta:
        ordering = ['id']
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def save(self, *args, **kwargs):
        from apps.project.elasticsearch import ProjectElasticSearchModelService
        refresh = kwargs.pop('refresh', False)
        add_to_es = kwargs.pop('add_to_es', False)
        super(Project, self).save(*args, **kwargs)
        if add_to_es:
            ProjectElasticSearchModelService().indexing_model(self, refresh)

    @property
    def is_url_working(self):
        return not bool(self.notes)

    def __str__(self):
        return f'{self.pk}-{self.name}'
