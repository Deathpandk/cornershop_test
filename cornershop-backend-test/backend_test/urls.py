"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.employees.urls import EMPLOYEES_ROUTER
from apps.menu.urls import MENU_ROUTER

from .utils.healthz import healthz

API_ROUTER = DefaultRouter()

API_ROUTER.registry.extend(EMPLOYEES_ROUTER.registry)
API_ROUTER.registry.extend(MENU_ROUTER.registry)

urlpatterns = [
    path("healthz", healthz, name="healthz"),
    path("api/", include((API_ROUTER.urls, "api"))),
]
