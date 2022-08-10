from rest_framework import serializers

from apps.employees.serializers import OrderSerializer

from .models import Menu, MenuOption


class MenuOptionSerializer(serializers.ModelSerializer):
    """Serializer for menu option endpoint"""

    class Meta:
        model = MenuOption
        fields = ["name", "description", "menu", "pk"]
        read_only_fields = ["pk"]
        extra_kwargs = {"menu": {"write_only": True}}


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for menu endpoint with options"""

    options = MenuOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ["date", "options", "pk"]
        read_only_fields = ["pk"]


class MenuWithOrdersSerializer(MenuSerializer):
    """Serializer for menu including orders"""

    orders = OrderSerializer(many=True, read_only=True)

    class Meta(MenuSerializer.Meta):
        fields = ["date", "options", "orders", "pk"]
