from rest_framework.routers import SimpleRouter

from .views import EmployeeViewSet

EMPLOYEES_ROUTER = SimpleRouter()

EMPLOYEES_ROUTER.register("employees", EmployeeViewSet, "employees")
