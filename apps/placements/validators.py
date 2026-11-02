from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_size(file):
    limit_mb = settings.DOCUMENT_MAX_UPLOAD_MB
    if file.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Files may not be larger than {limit_mb} MB.")
