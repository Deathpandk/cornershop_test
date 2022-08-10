import datetime
from unittest.mock import patch

from django.test import TestCase
from rest_framework.serializers import ValidationError

from schema import Schema

from apps.employees.factories import EmployeeFactory
from apps.employees.models import Employee, Order
from apps.employees.serializers import EmployeeSerializer, OrderSerializer
from apps.menu.factories import MenuFactory, MenuOptionFactory
from apps.menu.models import MenuUUID
from backend_test.utils.slack import simulate_error

EMPLOYEE_SCHEMA = {
    "name": str,
    "slack_id": str,
}

EMPLOYEE_DATA = {"name": "Generic Name", "slack_id": "SlackId"}

ORDER_SCHEMA = {
    "name": str,
    "date": str,
    "choice": str,
    "comments": str,
}


class EmployeeSerializerTest(TestCase):
    """Tests for Employee Serializer"""

    def setUp(self) -> None:
        self.employee = EmployeeFactory()

    def test_serializer_schema(self):
        """Test Employee Serializer Schema"""

        serializer = EmployeeSerializer(self.employee)

        schema = Schema(EMPLOYEE_SCHEMA)
        schema.validate(dict(serializer.data))

    @patch("apps.employees.utils.slack_client.chat_postMessage")
    def test_serializer_create(self, mocked_post_message):
        """Test serializer create"""

        serializer = EmployeeSerializer(data=EMPLOYEE_DATA)
        serializer.is_valid(True)
        instance = serializer.save()

        self.assertTrue(isinstance(instance, Employee))
        self.assertEqual(instance.name, EMPLOYEE_DATA.get("name"))
        self.assertEqual(instance.slack_id, EMPLOYEE_DATA.get("slack_id"))

    def test_serializer_with_existing_id_value(self):
        """Test serializer with existing slack_id"""

        data = EMPLOYEE_DATA.copy()
        data["slack_id"] = self.employee.slack_id
        with self.assertRaises(ValidationError) as error:
            serializer = EmployeeSerializer(data=data)
            serializer.is_valid(True)
        self.assertIn("this slack id already exists", str(error.exception))

    def test_serializer_with_long_slack_id_value(self):
        """Test serializer with more than 16 characters as slack_id value"""

        data = EMPLOYEE_DATA.copy()
        data["slack_id"] = "I" * 17
        with self.assertRaises(ValidationError) as error:
            serializer = EmployeeSerializer(data=data)
            serializer.is_valid(True)
        self.assertIn("no more than 16", str(error.exception))

    @patch(
        "apps.employees.utils.slack_client.chat_postMessage", side_effect=simulate_error
    )
    def test_serializer_with_invalid_slack_id(self, mocked_post_message):
        """Test serializer with invalid slack_id"""

        with self.assertRaises(ValidationError) as error:
            serializer = EmployeeSerializer(data=EMPLOYEE_DATA)
            serializer.is_valid(True)
        error = error.exception.detail.get("non_field_errors")[0]
        self.assertEqual(str(error), "Invalid Slack Id")

    def test_serializer_with_long_name_value(self):
        """Test serializer with more than 32 characters as name value"""

        data = EMPLOYEE_DATA.copy()
        data["name"] = "N" * 33
        with self.assertRaises(ValidationError) as error:
            serializer = EmployeeSerializer(data=data)
            serializer.is_valid(True)
        self.assertIn("no more than 32", str(error.exception))


class OrderSerializerTest(TestCase):
    """Tests for Order Serializer"""

    def setUp(self):
        self.employee = EmployeeFactory()
        self.option = MenuOptionFactory()
        self.menu = self.option.menu
        self.menu_uuid = MenuUUID.objects.create(
            menu=self.menu,
            employee=self.employee,
        )
        self.data = {
            "uuid": self.menu_uuid.uuid,
            "option": self.option.pk,
            "comments": "Some specification",
        }

        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.tomorrow_menu = MenuFactory(date=tomorrow)
        self.tomorrow_option = MenuOptionFactory(menu=self.tomorrow_menu)
        self.tomorrow_menu_uuid = MenuUUID.objects.create(
            menu=self.tomorrow_menu,
            employee=self.employee,
        )

    @patch(
        "apps.employees.serializers.OrderSerializer._get_current_hour", return_value=10
    )
    def test_serializer_create_and_schema(self, mocked_hour):
        """Test serializer create and data schema"""

        serializer = OrderSerializer(data=self.data)
        serializer.is_valid(True)
        instance = serializer.save()

        self.assertTrue(isinstance(instance, Order))
        self.assertEqual(instance.menu, self.menu)
        self.assertEqual(instance.employee, self.employee)
        self.assertEqual(instance.option, self.option)
        self.assertEqual(instance.comments, self.data.get("comments"))

        serializer = OrderSerializer(instance)
        schema = Schema(ORDER_SCHEMA)
        schema.validate(dict(serializer.data))

    @patch(
        "apps.employees.serializers.OrderSerializer._get_current_hour", return_value=10
    )
    def test_serializer_with_option_from_different_menu(self, mocked_date):
        """Test serializer create and data schema"""

        self.data["option"] = self.tomorrow_option.pk

        with self.assertRaises(ValidationError) as error:
            serializer = OrderSerializer(data=self.data)
            serializer.is_valid(True)
        error = error.exception.detail.get("non_field_errors")[0]
        self.assertEqual(str(error), "Selected option dont belongs to menu")

    @patch(
        "apps.employees.serializers.OrderSerializer._get_current_hour", return_value=10
    )
    def test_serializer_with_tomorrow_menu(self, mocked_date):
        """Test serializer create and data schema"""

        self.data["uuid"] = self.tomorrow_menu_uuid.uuid

        with self.assertRaises(ValidationError) as error:
            serializer = OrderSerializer(data=self.data)
            serializer.is_valid(True)
        error = error.exception.detail.get("non_field_errors")[0]
        self.assertEqual(str(error), "Only Orders for today menu available")

    @patch(
        "apps.employees.serializers.OrderSerializer._get_current_hour", return_value=11
    )
    def test_serializer_for_after_11_am(self, mocked_date):
        """Test serializer after 11 am"""

        with self.assertRaises(ValidationError) as error:
            serializer = OrderSerializer(data=self.data)
            serializer.is_valid(True)
        error = error.exception.detail.get("non_field_errors")[0]
        self.assertEqual(str(error), "Orders only available before 11am")
