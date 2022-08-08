from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    """Nora's employee viewset"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
