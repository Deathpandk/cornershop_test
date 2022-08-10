from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.employees.factories import EmployeeFactory
from apps.menu.factories import MenuOptionFactory
from apps.menu.models import MenuUUID
from backend_test.testing import APITestCaseWithLogin
from backend_test.utils.slack import simulate_error

from .test_serializers import EMPLOYEE_DATA


class EmployeeViewSetListTest(APITestCaseWithLogin):
    """Test Employee Endpoints"""

    def setUp(self):
        super(EmployeeViewSetListTest, self).setUp()
        self.employee = EmployeeFactory()

    def list_employees(self):
        """Call List Endpoint"""

        url = reverse("api:employees-list")

        return self.client.get(url)

    def test_list_endpoint(self):
        """Test List endpoint with anonymous user, expect a 403 error"""
        self.login()
        response = self.list_employees()

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

    def test_list_endpoint_with_anonymous_user(self):
        """Test List endpoint with anonymous user, expect a 403 error"""

        response = self.list_employees()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )


class EmployeeViewSetCreateTest(APITestCaseWithLogin):
    """Test Employee Endpoints"""

    def setUp(self):
        super(EmployeeViewSetCreateTest, self).setUp()
        self.employee = EmployeeFactory()

    def create_employee(self, data):
        """Call Create Endpoint"""

        url = reverse("api:employees-list")

        return self.client.post(url, data)

    @patch("apps.employees.utils.slack_client.chat_postMessage")
    def test_create_endpoint(self, mocked_post_message):
        """Test Create endpoint with logged user"""
        self.login()
        response = self.create_employee(EMPLOYEE_DATA)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    @patch(
        "apps.employees.utils.slack_client.chat_postMessage", side_effect=simulate_error
    )
    def test_create_endpoint_with_invalid_slack_id(self, mocked_post_message):
        """Test Create endpoint with logged user"""
        self.login()

        response = self.create_employee(EMPLOYEE_DATA)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.json()
        )
        self.assertEqual("Invalid Slack Id", response.json().get("non_field_errors")[0])

    def test_create_endpoint_with_existing_slack_id(self):
        """Test Create endpoint with existing slack id, expect a 400 error"""
        self.login()
        data = EMPLOYEE_DATA.copy()
        data["slack_id"] = self.employee.slack_id
        response = self.create_employee(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("slack_id", response.json())

    def test_create_endpoint_with_long_slack_id(self):
        """Test Create endpoint with more than 16 characters slack id, expect a 400 error"""
        self.login()
        data = EMPLOYEE_DATA.copy()
        data["slack_id"] = "I" * 17
        response = self.create_employee(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("slack_id", response.json())

    def test_create_endpoint_with_long_name(self):
        """Test Create endpoint with more than 32 characters name, expect a 400 error"""
        self.login()
        data = EMPLOYEE_DATA.copy()
        data["name"] = "N" * 33
        response = self.create_employee(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.json())

    def test_create_endpoint_with_anonymous_user(self):
        """Test Create endpoint with anonymous user, expect a 403 error"""

        response = self.create_employee(EMPLOYEE_DATA)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )


class OrderViewSetCreateTest(APITestCase):
    """Tests for Order View Set"""

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

    def create_order(self, data):
        """Call Create Endpoint"""

        url = reverse("api:orders-list")

        return self.client.post(url, data)

    @patch(
        "apps.employees.serializers.OrderSerializer._get_current_hour", return_value=10
    )
    def test_create_endpoint(self, mocked_date):
        """Test Create endpoint with logged user"""

        response = self.create_order(self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
