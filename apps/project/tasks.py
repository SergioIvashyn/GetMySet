from __future__ import absolute_import, unicode_literals

from typing import Optional

from celery import shared_task
from django.utils.timezone import now

from apps.accounts.models import User
from apps.project.utils import ProjectImportService
from demo.celery import app

# Simple task


@app.task
def save_projects_from_csv(data: str, user_id: Optional[int], input_format_int: int):
    project_import_service = ProjectImportService()

    import_formats = project_import_service.get_import_formats()
    input_format = import_formats[input_format_int]()
    dataset = input_format.create_dataset(data)
    user = User.objects.filter(pk=user_id).first()
    resource = project_import_service.get_import_resource_class()(user=user)
    result = resource.import_data(dataset, dry_run=False, raise_errors=False)


@shared_task
def execute_scenario_shared_task():
    print(now())
