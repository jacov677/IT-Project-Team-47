from django.db import models


class HostOrganization(models.Model):
    """Organisation that hosts WIL placements (table: host_organization)."""

    organisation_id = models.AutoField(primary_key=True)
    organisation_name = models.CharField(max_length=150)
    registration_number = models.CharField(max_length=80, unique=True, null=True, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(max_length=150, blank=True)

    class Meta:
        db_table = "host_organization"
        ordering = ["organisation_name"]
        verbose_name = "host organisation"

    def __str__(self):
        return self.organisation_name
