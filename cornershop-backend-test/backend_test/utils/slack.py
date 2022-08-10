from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from backend_test.envtools import getenv

slack_client = WebClient(token=getenv("SLACK_TOKEN"))


def simulate_error(*args, **kwargs):
    """Method to simulate SlackAPIError in testing"""
    raise SlackApiError("simulate_error", {})
