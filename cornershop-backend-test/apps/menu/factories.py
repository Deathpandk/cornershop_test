from datetime import date

from factory import SubFactory
from factory.django import DjangoModelFactory


class MenuFactory(DjangoModelFactory):
    """Factory for Menu model testing"""

    date = date.today()

    class Meta:
        model = "menu.Menu"


class MenuOptionFactory(DjangoModelFactory):
    """Factory for menu option with menu subfactory"""

    menu = SubFactory(MenuFactory)
    name = "Menu Option"
    description = "Some Tasty menu option"

    class Meta:
        model = "menu.MenuOption"
