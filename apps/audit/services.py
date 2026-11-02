from .models import AuditLog


def log_action(user, action, instance=None, *, table_name=None, record_id=None):
    """Record who did what to which record (section 4.5, Audit Trail).

    Pass a model instance, or give table_name and record_id yourself:

        log_action(request.user, "Approve placement", placement)
        log_action(request.user, "Generate report", table_name="report", record_id="placement_summary")
    """
    if instance is not None:
        table_name = instance._meta.db_table
        record_id = instance.pk
    if not table_name or record_id is None:
        raise ValueError("log_action needs a model instance or both table_name and record_id.")
    return AuditLog.objects.create(user=user, action=action[:80], table_name=table_name, record_id=str(record_id))
