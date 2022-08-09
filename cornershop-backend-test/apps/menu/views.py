from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend

from .models import Menu
from .serializers import MenuOptionSerializer, MenuSerializer


class MenuViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    """Nora's menu viewset"""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]


class MenuOptionViewSet(GenericViewSet, CreateModelMixin):
    """Nora's menu options viewset"""

    serializer_class = MenuOptionSerializer
    permission_classes = [IsAuthenticated]
