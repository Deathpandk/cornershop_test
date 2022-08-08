from django.db import models


class Employee(models.Model):
    """Model for employee register"""

    name = models.CharField(max_length=32)
    slack_id = models.CharField(max_length=16, unique=True)
