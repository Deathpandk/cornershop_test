from django.db import DataError, IntegrityError
from django.test import TestCase

from apps.employees.factories import EmployeeFactory
from apps.employees.models import Employee


class EmployeeModelTest(TestCase):
    """Tests for Employee Model"""

    def test_create_employee(self):
        """Test create employee"""

        Employee.objects.create(name="Generic Name", slack_id="SLACK_ID")
        self.assertTrue(Employee.objects.exists())

    def test_create_employee_with_existing_slack_id(self):
        """Test raises error when creating employee with existing slack id"""

        employee = EmployeeFactory()
        with self.assertRaises(IntegrityError) as error:
            Employee.objects.create(name="Name", slack_id=employee.slack_id)
        self.assertIn("duplicate key value", str(error.exception))
        self.assertIn("slack_id", str(error.exception))

    def test_create_employee_with_long_slack_id(self):
        """Test raises error when creating employee with more than 16 characters as ID"""

        with self.assertRaises(DataError) as error:
            Employee.objects.create(name="Name", slack_id="I" * 17)
        self.assertIn("value too long", str(error.exception))

    def test_create_employee_with_long_name(self):
        """Test raises error when creating employee with more than 32 characters as name"""

        with self.assertRaises(DataError) as error:
            Employee.objects.create(name="N" * 33, slack_id="ID")
        self.assertIn("value too long", str(error.exception))
