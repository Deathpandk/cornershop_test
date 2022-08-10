from django.contrib.auth.views import LoginView as BaseLogin
from django.urls import reverse
from django.views.generic import TemplateView


class LoginView(BaseLogin):
    def get_success_url(self):
        return reverse("webpage:administration")


class EmployeeMenu(TemplateView):
    template_name = "employee_menu.html"


class Administration(TemplateView):
    template_name = "administration.html"
