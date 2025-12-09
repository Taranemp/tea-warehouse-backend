
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.shortcuts import redirect


schema_view = get_schema_view(
    openapi.Info(
        title="TeaTrace API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls, name="admin page"),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-auth/', include('rest_framework.urls')),
    # re_path(r'^$', lambda request: redirect('/api/v1/', permanent=False)),
    # path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),



    path('api/v1/', include('account.urls')),
    path('', lambda request: redirect('schema-swagger-ui', permanent=False), name="index page"),
        

]