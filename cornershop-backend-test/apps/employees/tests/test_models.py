from django.db import DataError, IntegrityError
from django.test import TestCase

from apps.employees.factories import EmployeeFactory
from apps.employees.models import Employee, Order
from apps.menu.factories import MenuOptionFactory


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


class OrderModelTest(TestCase):
    """Tests for Order Model"""

    def setUp(self):
        self.option = MenuOptionFactory()
        self.employee = EmployeeFactory()

    def test_create_order(self):
        """Test create order"""

        Order.objects.create(
            menu=self.option.menu,
            option=self.option,
            employee=self.employee,
            comments="With salad",
        )
        self.assertTrue(Order.objects.exists())

    def test_create_order_without_comments(self):
        """Test create order with no comments"""

        Order.objects.create(
            menu=self.option.menu,
            option=self.option,
            employee=self.employee,
        )
        self.assertTrue(Order.objects.exists())

    def test_create_order_with_existing_employee_menu(self):
        """Test raises error when creating order with existing employee-menu"""

        Order.objects.create(
            menu=self.option.menu,
            option=self.option,
            employee=self.employee,
            comments="With salad",
        )
        with self.assertRaises(IntegrityError) as error:
            Order.objects.create(
                menu=self.option.menu,
                option=self.option,
                employee=self.employee,
                comments="With salad",
            )
        self.assertIn("duplicate key value", str(error.exception))
