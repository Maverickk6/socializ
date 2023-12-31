from django.contrib import admin
from django.urls import path, include
from features.userAuth.views import LoginView

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework import permissions
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Socializ API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # swagger
    re_path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("", include("features.userAuth.urls")),
    path("", include("features.post.urls")),
    path("", include("features.comments.urls")),
    # Simple jwt
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Login
    path("login/", LoginView.as_view(), name="login"),
    # viewsets
    path("", include("features.userAuth.routers")),
    path("", include("features.post.routers")),
    path("", include("features.comments.routers")),
]
