from django.core.exceptions import PermissionDenied, ValidationError


class BusinessRuleError(ValidationError):
    """Raised when an action breaks one of the Phase 3 / 4.5 business rules.

    Views catch this and show the message to the user, e.g.:

        try:
            approve_placement(placement, request.user)
        except BusinessRuleError as error:
            messages.error(request, error.message)
    """


class NotAllowed(PermissionDenied):
    """Raised when a user tries to act on a record that is not theirs."""
