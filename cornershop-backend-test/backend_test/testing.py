from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class APITestCaseWithLogin(APITestCase):
    """APITestCase with login auxiliar method"""

    def setUp(self):
        self.user_credentials = {"username": "Nora", "password": "cornershop"}
        user = User.objects.create(username=self.user_credentials.get("username"))
        user.set_password(self.user_credentials.get("password"))
        user.save()

    def login(self):
        """Login with authenticated user"""

        self.client.login(**self.user_credentials)
