
from django.db import models


class HostOrganization(models.Model):
    organisation_id = models.AutoField(primary_key=True)

    organisation_name = models.CharField(max_length=150)

    registration_number = models.CharField(
        max_length=80,
        unique=True,
        null=True,
        blank=True,
    )

    industry = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_email = models.EmailField(max_length=150)

    contact_number = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organisations_hostorganization"
        ordering = ["organisation_name"]
        indexes = [
            models.Index(
                fields=["organisation_name"],
                name="org_name_idx",
            ),
            models.Index(
                fields=["industry"],
                name="org_industry_idx",
            ),
        ]

    def __str__(self):
        return self.organisation_name
