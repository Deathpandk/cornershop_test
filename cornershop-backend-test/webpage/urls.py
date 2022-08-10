from django.urls import path

from webpage.views import Administration, EmployeeMenu, LoginView

app_name = "webpage"
urlpatterns = [
    path("", LoginView.as_view(), name="home"),
    path("administration", Administration.as_view(), name="administration"),
    path("menu/<uuid:uuid>/", EmployeeMenu.as_view(), name="employee-menu"),
]
