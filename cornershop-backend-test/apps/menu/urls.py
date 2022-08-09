from rest_framework.routers import SimpleRouter

from .views import MenuOptionViewSet, MenuViewSet

MENU_ROUTER = SimpleRouter()

MENU_ROUTER.register("menu", MenuViewSet, "menu")
MENU_ROUTER.register("menuoption", MenuOptionViewSet, "menuoption")
