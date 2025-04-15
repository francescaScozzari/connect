"""The xai app urls."""

from django.urls import include, path
from rest_framework import routers

from xai.views import AuthorsSearchView

app_name = "xai"

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("author/search/", AuthorsSearchView.as_view()),
]
