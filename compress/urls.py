from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Sniffs API",
        default_version='v1',
        description="API documentation for Sniffs APP",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@touristapp.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('user/', include('authAPI.urls')),
    path('product/', include('productsAPI.urls')),
    path('contract/', include('contractAPI.urls')),
    path('bill/', include('billAPI.urls')),
    path('comment/', include('commentAPI.urls')),
    path('cart/', include('cartAPI.urls')),
    path('quotation/', include('quotation.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)