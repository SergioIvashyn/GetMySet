from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from apps.project.elasticsearch import ProjectElasticSearchModelService
from apps.core.models import Project


@receiver(pre_delete, sender=Project)
def es_handle_delete_project(sender, instance, **kwargs):
    ProjectElasticSearchModelService().remove_model_from_index(instance)


@receiver(m2m_changed, sender=Project.industries.through)
def es_project_industries_changed(sender, instance, **kwargs):
    ProjectElasticSearchModelService().indexing_model(instance)


@receiver(m2m_changed, sender=Project.technologies.through)
def es_project_technologies_changed(sender, instance, **kwargs):
    ProjectElasticSearchModelService().indexing_model(instance)
