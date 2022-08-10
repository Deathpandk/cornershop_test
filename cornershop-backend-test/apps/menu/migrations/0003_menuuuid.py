# Generated by Django 3.0.8 on 2022-08-09 00:31
import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0001_initial"),
        ("menu", "0002_auto_20220808_2155"),
    ]

    operations = [
        migrations.CreateModel(
            name="MenuUUID",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="employees.Employee",
                    ),
                ),
                (
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="menu.Menu",
                    ),
                ),
            ],
            options={
                "unique_together": {("menu", "employee")},
            },
        ),
    ]
