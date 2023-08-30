"""The universities app urls."""

from django.urls import include, path
from rest_framework import routers

from universities.views import SearchAuthorViewSet

app_name = ""

router = routers.DefaultRouter()
router.register(r"author/search", SearchAuthorViewSet)

urlpatterns = [path("", include(router.urls))]
