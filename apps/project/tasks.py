from __future__ import absolute_import, unicode_literals

from typing import Optional
from django.utils.translation import ugettext_lazy as _

from celery import shared_task
from django.utils.timezone import now

from apps.accounts.models import User
from apps.core.models import ImportInfo
from apps.project.utils import ProjectImportService
from demo.celery import app


# Simple task


@app.task
def save_projects_from_csv(data: str, user_id: Optional[int], input_format_int: int):
    user = User.objects.filter(pk=user_id).first()
    import_info = None
    if user:
        import_info = ImportInfo.objects.create(user=user)
    project_import_service = ProjectImportService()

    import_formats = project_import_service.get_import_formats()
    input_format = import_formats[input_format_int]()
    dataset = input_format.create_dataset(data)
    resource = project_import_service.get_import_resource_class()(user=user)
    result = resource.import_data(dataset, dry_run=False, raise_errors=False)
    if import_info:
        if not result.has_validation_errors() or result.has_errors():
            import_info.status = ImportInfo.SUCCESS
            import_info.message =\
                _('Import finished, with %(new)d new and %(update)d updated Projects.') % result.totals
        else:
            import_info.status = ImportInfo.FAILED
            import_info.message = ImportInfo.FAILED
        import_info.save(update_fields=['status', 'message'])


@shared_task
def execute_scenario_shared_task():
    print(now())
