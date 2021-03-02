from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apps.project.elasticsearch import ProjectElasticSearchModelService
from apps.core.models import Project


@receiver(post_save, sender=Project)
def es_handle_create_project(sender, instance, created, **kwargs):
    ProjectElasticSearchModelService().indexing_model(instance)


@receiver(pre_delete, sender=Project)
def es_handle_delete_project(sender, instance, **kwargs):
    ProjectElasticSearchModelService().remove_model_from_index(instance)
