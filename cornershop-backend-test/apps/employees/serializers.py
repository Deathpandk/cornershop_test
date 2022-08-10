from rest_framework import serializers

from .models import Employee
from .utils import validate_employee_data


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employee endpoint"""

    class Meta:
        model = Employee
        fields = ["name", "slack_id"]

    def validate(self, attrs):
        name, slack_id = attrs.get("name"), attrs.get("slack_id")
        if not validate_employee_data(name, slack_id):
            raise serializers.ValidationError("Invalid Slack Id")

        return attrs
