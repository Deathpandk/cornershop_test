from django.db import models


class Menu(models.Model):
    """Model to represent a day menu"""

    date = models.DateField(unique=True)


class MenuOption(models.Model):
    """Model for a menu's choice option"""

    menu = models.ForeignKey("menu.Menu", on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, null=True, blank=True)
