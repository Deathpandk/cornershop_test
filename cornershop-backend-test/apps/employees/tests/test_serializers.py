from django.test import TestCase
from rest_framework.serializers import ValidationError

from schema import Schema

from apps.employees.factories import EmployeeFactory
from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer

EMPLOYEE_SCHEMA = {
    "name": str,
    "slack_id": str,
}

EMPLOYEE_DATA = {"name": "Generic Name", "slack_id": "SlackId"}


class EmployeeSerializerTest(TestCase):
    """Tests for Employee Serializer"""

    def setUp(self) -> None:
        self.employee = EmployeeFactory()

    def test_serializer_schema(self):
        """Test Employee Serializer Schema"""

        serializer = EmployeeSerializer(self.employee)

        schema = Schema(EMPLOYEE_SCHEMA)
        schema.validate(dict(serializer.data))

    def test_serializer_create(self):
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

    def test_serializer_with_long_name_value(self):
        """Test serializer with more than 32 characters as name value"""

        data = EMPLOYEE_DATA.copy()
        data["name"] = "N" * 33
        with self.assertRaises(ValidationError) as error:
            serializer = EmployeeSerializer(data=data)
            serializer.is_valid(True)
        self.assertIn("no more than 32", str(error.exception))
