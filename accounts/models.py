from django.db import models
from django.contrib.auth.models import AbstractUser

from home.models import Vulnerability

class User(AbstractUser):
    marked_vulnerabilities = models.ManyToManyField(Vulnerability)
    previous_login = models.DateTimeField(blank=True, null=True)

