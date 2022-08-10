from unittest.mock import patch

from django.test import TestCase

from slack_sdk.errors import SlackApiError

from apps.employees.factories import EmployeeFactory
from apps.menu.factories import MenuFactory
from apps.menu.models import MenuUUID
from apps.menu.utils import create_uuids, send_uuids_as_slack_message


class MenuUUIDutilsTest(TestCase):
    """Tests for Menu UUID utils"""

    def setUp(self):
        self.menu = MenuFactory()
        self.employee = EmployeeFactory()
        self.employee_2 = EmployeeFactory()

    def test_create_menu_uuids(self):
        """Test create menu uuids"""

        uuids = create_uuids(self.menu)

        self.assertEqual(len(uuids), 2)

        for item in uuids:
            self.assertIsInstance(item, MenuUUID)

        for employee in [self.employee, self.employee_2]:
            self.assertTrue(
                MenuUUID.objects.filter(employee=employee, menu=self.menu).exists()
            )

    @patch("apps.menu.utils.slack_client.chat_postMessage")
    def test_send_uuids_as_slack_message(self, mocked_post_message):
        """Test send uuids as slack message with a fail and a success"""

        uuid = MenuUUID.objects.create(menu=self.menu, employee=self.employee)
        uuid_2 = MenuUUID.objects.create(menu=self.menu, employee=self.employee_2)

        def send_message(channel, text):
            if channel == uuid_2.employee.slack_id:
                assert str(uuid_2.uuid) in text
                raise SlackApiError("simulate_error", {})
            else:
                assert str(uuid.uuid) in text

        mocked_post_message.side_effect = send_message

        fails = send_uuids_as_slack_message([uuid, uuid_2])
        self.assertEqual(fails, [uuid_2])

        self.assertEqual(len(mocked_post_message.mock_calls), 2)
