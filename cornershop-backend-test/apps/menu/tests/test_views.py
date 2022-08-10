from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from apps.employees.factories import EmployeeFactory
from apps.menu.factories import MenuFactory
from backend_test.testing import APITestCaseWithLogin

from .test_serializers import MENU_DATA


class MenuViewSetListTest(APITestCaseWithLogin):
    """Test Menu List Endpoint"""

    def setUp(self):
        super(MenuViewSetListTest, self).setUp()
        self.menu = MenuFactory()

    def list_menu(self):
        """Call List Endpoint"""

        url = reverse("api:menu-list")

        return self.client.get(url)

    def test_list_endpoint(self):
        """Test List endpoint with anonymous user, expect a 403 error"""
        self.login()
        response = self.list_menu()

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

    def test_list_endpoint_with_anonymous_user(self):
        """Test List endpoint with anonymous user, expect a 403 error"""

        response = self.list_menu()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )


class MenuViewSetCreateTest(APITestCaseWithLogin):
    """Test Menu Create Endpoint"""

    def setUp(self):
        super(MenuViewSetCreateTest, self).setUp()
        self.menu = MenuFactory()

    def create_menu(self, data):
        """Call Create Endpoint"""

        url = reverse("api:menu-list")

        return self.client.post(url, data)

    def test_create_endpoint(self):
        """Test Create endpoint with logged user"""
        self.login()
        response = self.create_menu(MENU_DATA)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    def test_create_endpoint_with_existing_date(self):
        """Test Create endpoint with existing date, expect a 400 error"""
        self.login()
        response = self.create_menu({"date": self.menu.date})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.json())

    def test_create_endpoint_with_anonymous_user(self):
        """Test Create endpoint with anonymous user, expect a 403 error"""

        response = self.create_menu(MENU_DATA)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )


class MenuViewSetRemindersTest(APITestCaseWithLogin):
    """Test Reminders endpoint to consume celery task"""

    def setUp(self):
        super(MenuViewSetRemindersTest, self).setUp()
        self.menu = MenuFactory()
        self.employee = EmployeeFactory(slack_id="U02H6L5A2G0")
        self.employee_2 = EmployeeFactory()

    def send_reminders(self, menu):
        """Call Send Reminders Endpoint"""

        url = reverse("api:menu-reminders", args=[menu.pk])

        return self.client.post(url, {})

    @patch("apps.menu.celery_tasks.create_and_send_uuids.delay")
    def test_send_reminders(self, mocked_celery):
        """Test Send Reminders Endpoint"""

        self.login()
        response = self.send_reminders(self.menu)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mocked_celery.assert_called_once()

    def test_reminders_endpoint_with_anonymous_user(self):
        """Test Reminders endpoint with anonymous user, expect a 403 error"""

        response = self.send_reminders(self.menu)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )
