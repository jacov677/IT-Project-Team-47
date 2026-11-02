"""Accounts module.

Phase 4 section 4.5 tables for this module: user, student, coordinator, mentor.

The custom User model below is deliberately empty. Django requires a custom user
model to be set up before the first migration, otherwise it cannot be changed later.
The accounts owner adds the role field and profile models here.
"""
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
