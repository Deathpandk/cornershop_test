from uuid import uuid4

from django.db import models


class Menu(models.Model):
    """Model to represent a day menu"""

    date = models.DateField(unique=True)


class MenuOption(models.Model):
    """Model for a menu's choice option"""

    menu = models.ForeignKey(
        "menu.Menu", on_delete=models.CASCADE, related_name="options"
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, null=True, blank=True)


class MenuUUID(models.Model):
    """Model to store UUID's for employees"""

    uuid = models.UUIDField(primary_key=True, default=uuid4)
    employee = models.ForeignKey("employees.Employee", on_delete=models.CASCADE)
    menu = models.ForeignKey("menu.Menu", on_delete=models.CASCADE)

    is_send = models.BooleanField(default=False)

    class Meta:
        unique_together = ("menu", "employee")
