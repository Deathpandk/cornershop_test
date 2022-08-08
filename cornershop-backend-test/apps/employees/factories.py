from factory import Sequence
from factory.django import DjangoModelFactory


class EmployeeFactory(DjangoModelFactory):
    """Factory for Employee model testing"""

    name = "Employee's name"
    slack_id = Sequence(lambda n: f"ID{n}")

    class Meta:
        model = "employees.Employee"
