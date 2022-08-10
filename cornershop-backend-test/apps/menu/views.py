from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend

from .celery_tasks import create_and_send_uuids
from .models import Menu
from .serializers import MenuOptionSerializer, MenuSerializer


class MenuViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    """Nora's menu viewset"""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    @action(methods=["post"], detail=True)
    def reminders(self, request, pk):
        menu = self.get_object()
        create_and_send_uuids.delay(menu.pk)
        return Response()


class MenuOptionViewSet(GenericViewSet, CreateModelMixin):
    """Nora's menu options viewset"""

    serializer_class = MenuOptionSerializer
    permission_classes = [IsAuthenticated]
