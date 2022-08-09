from django.urls import reverse
from rest_framework import status

from apps.employees.factories import EmployeeFactory
from backend_test.testing import APITestCaseWithLogin

from .test_serializers import EMPLOYEE_DATA


class EmployeeViewSetTest(APITestCaseWithLogin):
    """Test Employee Endpoints"""

    def setUp(self):
        super(EmployeeViewSetTest, self).setUp()

        self.employee = EmployeeFactory()

    def list_employees(self):
        """Call List Endpoint"""

        url = reverse("api:employees-list")

        return self.client.get(url)

    def create_employee(self, data):
        """Call Create Endpoint"""

        url = reverse("api:employees-list")

        return self.client.post(url, data)

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

    def test_create_endpoint(self):
        """Test Create endpoint with logged user"""
        self.login()
        response = self.create_employee(EMPLOYEE_DATA)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

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
