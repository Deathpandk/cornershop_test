from slack_sdk.errors import SlackApiError

from apps.employees.models import Employee
from apps.menu.models import Menu, MenuUUID
from backend_test.envtools import getenv
from backend_test.utils.slack import slack_client

BASE_URL = getenv("BASE_URL")


def create_uuids(menu: Menu) -> [MenuUUID]:
    """Method to create MenuUUID objects with given menu for all employees"""

    objects = []
    for employee in Employee.objects.all():
        objects.append(
            MenuUUID(
                menu=menu,
                employee=employee,
            )
        )
    return MenuUUID.objects.bulk_create(objects)


def send_uuids_as_slack_message(uuids: [MenuUUID]) -> [MenuUUID]:
    """Method to send uuids as slack messages"""

    fails = []
    for item in uuids:
        try:
            slack_client.chat_postMessage(
                channel=item.employee.slack_id,
                text=f"Hi, {item.employee.name}! You can found today's menu here: {BASE_URL}/menu/{item.uuid}",
            )
        except SlackApiError:
            fails.append(item)
    return fails
