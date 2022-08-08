from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employee endpoint"""

    class Meta:
        model = Employee
        fields = ["name", "slack_id"]
