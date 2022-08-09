from rest_framework import serializers

from .models import Menu, MenuOption


class MenuOptionSerializer(serializers.ModelSerializer):
    """Serializer for menu option endpoint"""

    class Meta:
        model = MenuOption
        fields = ["name", "description", "menu"]
        extra_kwargs = {"menu": {"write_only": True}}


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for menu endpoint with options"""

    options = MenuOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ["date", "options"]
