from import_export.admin import ImportMixin
from import_export.formats.base_formats import XLS, CSV

from apps.project.resource import ProjectResource


class ProjectImportService(ImportMixin):
    resource_class = ProjectResource
    formats = (CSV, XLS)
