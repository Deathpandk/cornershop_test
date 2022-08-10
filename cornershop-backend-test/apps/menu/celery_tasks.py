from apps.menu.models import Menu
from apps.menu.utils import create_uuids, send_uuids_as_slack_message
from backend_test.celery import app


@app.task
def create_and_send_uuids(menu_pk: int):
    menu = Menu.objects.get(pk=menu_pk)

    uuids = create_uuids(menu)

    send_uuids_as_slack_message(uuids)
