from django.db import models


class Employee(models.Model):
    """Model for employee register"""

    name = models.CharField(max_length=32)
    slack_id = models.CharField(max_length=16, unique=True)


class Order(models.Model):
    """Model to register employee menu election"""

    employee = models.ForeignKey("employees.Employee", on_delete=models.CASCADE)
    menu = models.ForeignKey(
        "menu.Menu", on_delete=models.PROTECT, related_name="orders"
    )
    option = models.ForeignKey("menu.MenuOption", on_delete=models.PROTECT)

    comments = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        unique_together = ["menu", "employee"]
