from apps.menu.models import Menu
from apps.menu.utils import create_uuids, send_uuids_as_slack_message
from backend_test.celery import app


@app.task(bind=True)
def create_and_send_uuids(self, menu_pk: int):
    try:
        menu = Menu.objects.get(pk=menu_pk)
        uuids = create_uuids(menu)
        fails = send_uuids_as_slack_message(uuids)

        if fails:
            raise Exception("Some messages have failed")
    except Exception as exc:
        self.retry(exc=exc, countdown=10)
