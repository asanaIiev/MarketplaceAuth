from django.contrib import admin
from django.urls import path, include

from django.conf.urls.i18n import i18n_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Marketplace Authentication',
        default_version='v1',
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path('', include('app.urls')),
    path('docs/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('accounts/', include('allauth.urls'))
)
