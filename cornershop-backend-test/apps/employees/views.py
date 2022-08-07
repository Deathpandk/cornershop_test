from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from .serializers import EmployeeSerializer


class EmployeeViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    """Nora's employee viewset"""
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
