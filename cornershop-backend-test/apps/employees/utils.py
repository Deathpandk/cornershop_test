from slack_sdk.errors import SlackApiError

from backend_test.envtools import getenv
from backend_test.utils.slack import slack_client

BASE_URL = getenv("BASE_URL")


def validate_employee_data(name: str, slack_id: str) -> bool:
    """Validate employee slack id by sending a welcome message"""

    try:
        slack_client.chat_postMessage(
            channel=slack_id,
            text=f"Hi, {name}! We have register your slack account to receive our menu.",
        )
    except SlackApiError:
        return False
    return True
