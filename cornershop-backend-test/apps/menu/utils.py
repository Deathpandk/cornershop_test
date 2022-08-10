from slack_sdk.errors import SlackApiError

from apps.employees.models import Employee
from apps.menu.models import Menu, MenuUUID
from backend_test.envtools import getenv
from backend_test.utils.slack import slack_client

BASE_URL = getenv("BASE_URL")


def create_uuids(menu: Menu) -> [MenuUUID]:
    """Method to create MenuUUID objects with given menu for all employees"""

    to_create = []
    existent = MenuUUID.objects.filter(menu=menu)
    for employee in Employee.objects.all():
        if not existent.filter(employee=employee).exists():
            to_create.append(
                MenuUUID(
                    menu=menu,
                    employee=employee,
                )
            )
    MenuUUID.objects.bulk_create(to_create)
    return MenuUUID.objects.filter(menu=menu)


def send_uuids_as_slack_message(uuids: [MenuUUID]) -> [MenuUUID]:
    """Method to send uuids as slack messages"""

    fails, success = [], []
    uuids = [item for item in uuids if not item.is_send]
    for item in uuids:
        try:
            slack_client.chat_postMessage(
                channel=item.employee.slack_id,
                text=f"Hi, {item.employee.name}! You can found {item.menu.date} menu here: {BASE_URL}/menu/{item.uuid}/",
            )
            item.is_send = True
            success.append(item)
        except SlackApiError:
            fails.append(item)
    MenuUUID.objects.bulk_update(success, ["is_send"])
    return fails
