from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Junior Backend Developer Project Task",
        default_version="v1",

        description="A comprehensive job listing platform with role-based access control",
        terms_of_service="https://www.jobsite.com/terms/",
        contact=openapi.Contact(email="contact@jobsite.com"),
        license=openapi.License(name="MIT License"),

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
   
    authentication_classes=(JWTAuthentication,), 
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/auth/", include("authapp.rest.urlss.urls")),

    path("api/v1/auth/register/", include("authapp.rest.urlss.register")),
    path("api/v1/auth/token/", include("authapp.rest.urlss.token")),

    path("api/v1/jobs/", include("job.rest.urls")),
]


urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_SWAGGER:
    urlpatterns += [
        path(
            "swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
