from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """One row per create, update or approval action (section 4.5, Audit Trail)."""

    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column="user_id", related_name="audit_logs"
    )
    action = models.CharField(max_length=80)
    table_name = models.CharField(max_length=80)
    record_id = models.CharField(max_length=80)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_log"
        ordering = ["-logged_at"]
        indexes = [models.Index(fields=["table_name", "record_id"], name="audit_record_idx")]

    def __str__(self):
        return f"{self.logged_at:%Y-%m-%d %H:%M} {self.user} {self.action} {self.table_name}#{self.record_id}"
