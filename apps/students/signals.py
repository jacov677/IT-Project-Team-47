"""Creates student notifications automatically when applications are submitted
or when the organisation / coordinator changes an application's status."""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Application, Notification

STATUS_MESSAGES = {
    Application.Status.UNDER_REVIEW: "The organisation is now reviewing your application",
    Application.Status.APPROVED: "Congratulations! Your application was approved",
    Application.Status.REJECTED: "Unfortunately your application was not successful",
}


@receiver(pre_save, sender=Application)
def remember_old_status(sender, instance, **kwargs):
    instance._old_status = (
        Application.objects.filter(pk=instance.pk).values_list("status", flat=True).first() if instance.pk else None
    )


@receiver(post_save, sender=Application)
def notify_student(sender, instance, created, **kwargs):
    user = instance.student.user
    opp = instance.opportunity
    org_name = opp.organisation.organisation_name
    if created:
        Notification.objects.create(
            user=user,
            title="Application submitted",
            message=f"Your application for {opp.title} at {org_name} was submitted.",
        )
        return
    old = getattr(instance, "_old_status", None)
    if old and old != instance.status and instance.status in STATUS_MESSAGES:
        Notification.objects.create(
            user=user,
            title=f"Application {instance.get_status_display().lower()}",
            message=f"{STATUS_MESSAGES[instance.status]} for {opp.title} at {org_name}.",
        )
