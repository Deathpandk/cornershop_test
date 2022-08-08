from django.utils import timezone

from factory.django import DjangoModelFactory


class MenuFactory(DjangoModelFactory):
    """Factory for Menu model testing"""

    date = timezone.datetime.today()

    class Meta:
        model = "menu.Menu"
