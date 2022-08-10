from unittest.mock import patch

from django.test import TestCase

from apps.employees.utils import validate_employee_data
from backend_test.utils.slack import simulate_error


class EmployeesUtilsTest(TestCase):
    """Tests for Employee utils"""

    @patch("apps.employees.utils.slack_client.chat_postMessage")
    def test_valid_data(self, mocked_post_message):
        """Test validate_employee_data"""

        result = validate_employee_data("NAME", "SLACKID")

        self.assertTrue(result)

    @patch(
        "apps.employees.utils.slack_client.chat_postMessage", side_effect=simulate_error
    )
    def test_invalid_data(self, mocked_post_message):
        """Test validate_employee_data when exception raised"""

        result = validate_employee_data("NAME", "SLACKID")

        self.assertFalse(result)
