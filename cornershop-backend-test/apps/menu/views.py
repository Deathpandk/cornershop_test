from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend

from apps.menu.models import MenuUUID

from .celery_tasks import create_and_send_uuids
from .models import Menu
from .serializers import MenuOptionSerializer, MenuSerializer, MenuWithOrdersSerializer


class MenuViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    """Nora's menu viewset"""

    queryset = Menu.objects.all()
    serializer_class = MenuWithOrdersSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    @action(methods=["post"], detail=True)
    def reminders(self, request, pk):
        menu = self.get_object()
        create_and_send_uuids.delay(menu.pk)
        return Response()

    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[AllowAny],
        url_path=r"(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    )
    def options(self, request, uuid):
        menu_uuid = MenuUUID.objects.get(uuid=uuid)
        serializer = MenuSerializer(menu_uuid.menu)
        return Response(serializer.data)


class MenuOptionViewSet(GenericViewSet, CreateModelMixin):
    """Nora's menu options viewset"""

    serializer_class = MenuOptionSerializer
    permission_classes = [IsAuthenticated]
