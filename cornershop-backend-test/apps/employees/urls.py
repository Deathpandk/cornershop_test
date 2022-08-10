from rest_framework.routers import SimpleRouter

from .views import EmployeeViewSet, PublicOrderViewSet

EMPLOYEES_ROUTER = SimpleRouter()

EMPLOYEES_ROUTER.register("employees", EmployeeViewSet, "employees")
EMPLOYEES_ROUTER.register("orders", PublicOrderViewSet, "orders")
