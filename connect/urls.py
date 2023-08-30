"""Connect URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.static import serve

from connect.views import HealthView

admin.site.site_header = admin.site.site_title = "Connect"

try:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
    )
except ModuleNotFoundError:  # pragma: no cover
    api_docs_urlpatterns = []  # pragma: no cover
    pass
else:  # pragma: no cover
    api_docs_urlpatterns = [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "docs/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"
        ),
    ]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            (
                [
                    path("", include("universities.urls")),
                    *api_docs_urlpatterns,
                ],
                "api",
            )
        ),
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("backend/health/", HealthView.as_view(), name="health-check"),
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]

try:
    import debug_toolbar
except ModuleNotFoundError:  # pragma: no cover
    pass
else:
    urlpatterns.append(
        path("__debug__/", include(debug_toolbar.urls))
    )  # pragma: no cover
