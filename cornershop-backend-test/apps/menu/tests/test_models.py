from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from apps.menu.factories import MenuFactory
from apps.menu.models import Menu, MenuOption


class MenuModelTest(TestCase):
    """Tests for Menu Model"""

    def test_create_menu(self):
        """Test create menu"""

        Menu.objects.create(date=timezone.datetime.today())
        self.assertTrue(Menu.objects.exists())

    def test_create_menu_with_existing_date(self):
        """Test raises error when creating menu with existing date"""

        menu = MenuFactory()
        with self.assertRaises(IntegrityError) as error:
            Menu.objects.create(date=menu.date)
        self.assertIn("duplicate key value", str(error.exception))
        self.assertIn("date", str(error.exception))


class MenuOptionModelTest(TestCase):
    """Test for MenuOption Model"""

    def setUp(self):
        self.menu = MenuFactory()

    def test_create_menuoption(self):
        """Test create Menu Option"""

        MenuOption.objects.create(
            menu=self.menu,
            name="Hamburger",
            description="Tasty Wonderful Hamburger Made with love",
        )
        self.assertTrue(MenuOption.objects.exists())
