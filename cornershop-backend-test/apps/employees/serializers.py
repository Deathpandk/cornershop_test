import datetime

from rest_framework import serializers

from apps.menu.models import MenuUUID

from .models import Employee, Order
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


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order creation"""

    uuid = serializers.UUIDField(write_only=True)
    date = serializers.DateField(source="menu.date", read_only=True)
    choice = serializers.CharField(source="option.name", read_only=True)
    name = serializers.CharField(source="employee.name", read_only=True)

    class Meta:
        model = Order
        fields = ["uuid", "option", "comments", "date", "choice", "name"]
        extra_kwargs = {
            "option": {"write_only": True},
        }

    def validate(self, attrs):
        uuid = attrs.get("uuid")
        menu_uuid = MenuUUID.objects.get(uuid=uuid)

        option = attrs.get("option")

        if menu_uuid.menu.date != datetime.date.today():
            raise serializers.ValidationError("Only Orders for today menu available")

        if self._get_current_hour() >= 11:
            raise serializers.ValidationError("Orders only available before 11am")

        if option.menu != menu_uuid.menu:
            raise serializers.ValidationError("Selected option dont belongs to menu")

        return attrs

    def _get_current_hour(self):
        """Auxiliar method to avoid errors when patching datetime"""
        return datetime.datetime.now().hour

    def create(self, validated_data):
        uuid = validated_data.get("uuid")
        menu_uuid = MenuUUID.objects.get(uuid=uuid)

        return Order.objects.create(
            employee=menu_uuid.employee,
            menu=menu_uuid.menu,
            option=validated_data.get("option"),
            comments=validated_data.get("comments", None),
        )
