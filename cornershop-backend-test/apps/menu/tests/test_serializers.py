from datetime import date

from django.test import TestCase
from rest_framework.serializers import ValidationError

from schema import Schema

from apps.employees.tests.test_serializers import ORDER_SCHEMA
from apps.menu.factories import MenuOptionFactory
from apps.menu.models import Menu, MenuOption
from apps.menu.serializers import (
    MenuOptionSerializer,
    MenuSerializer,
    MenuWithOrdersSerializer,
)

MENU_OPTION_SCHEMA = {
    "pk": int,
    "name": str,
    "description": str,
}

MENU_SCHEMA = {
    "pk": int,
    "date": str,
    "options": [MENU_OPTION_SCHEMA],
}

MENU_WITH_ORDERS_SCHEMA = {
    **MENU_SCHEMA,
    "orders": [ORDER_SCHEMA],
}

MENU_DATA = {"date": date(day=7, month=8, year=2022)}

MENU_OPTION_DATA = {"name": "Hamburger", "description": "Big Delicious Hamburger"}


class MenuSerializerTest(TestCase):
    """Tests for Menu with options Serializer"""

    def setUp(self):
        self.menuoption = MenuOptionFactory()
        self.menu = self.menuoption.menu

    def test_serializer_schema(self):
        """Test Menu Serializer Schema"""

        serializer = MenuSerializer(self.menu)

        schema = Schema(MENU_SCHEMA)
        schema.validate(dict(serializer.data))

    def test_serializer_schema_with_orders(self):
        """Test Menu Serializer Schema"""

        serializer = MenuWithOrdersSerializer(self.menu)

        schema = Schema(MENU_WITH_ORDERS_SCHEMA)
        schema.validate(dict(serializer.data))

    def test_serializer_create(self):
        """Test serializer create"""

        serializer = MenuSerializer(data=MENU_DATA)
        serializer.is_valid(True)
        instance = serializer.save()

        self.assertTrue(isinstance(instance, Menu))
        self.assertEqual(instance.date, MENU_DATA.get("date"))

    def test_serializer_with_existing_date(self):
        """Test serializer with existing date"""

        with self.assertRaises(ValidationError) as error:
            serializer = MenuSerializer(data={"date": self.menu.date})
            serializer.is_valid(True)
        self.assertIn("this date already exists", str(error.exception))


class MenuOptionSerializerTest(TestCase):
    """Tests for Menu Option Serializer"""

    def setUp(self):
        self.menuoption = MenuOptionFactory()

    def test_serializer_schema(self):
        """Test Menu Serializer Schema"""

        serializer = MenuOptionSerializer(self.menuoption)

        schema = Schema(MENU_OPTION_SCHEMA)
        schema.validate(dict(serializer.data))

    def test_serializer_create(self):
        """Test serializer create"""

        data = MENU_OPTION_DATA.copy()
        data["menu"] = self.menuoption.menu.pk
        serializer = MenuOptionSerializer(data=data)
        serializer.is_valid(True)
        instance = serializer.save()

        self.assertTrue(isinstance(instance, MenuOption))
        self.assertEqual(instance.name, MENU_OPTION_DATA.get("name"))
        self.assertEqual(instance.description, MENU_OPTION_DATA.get("description"))
