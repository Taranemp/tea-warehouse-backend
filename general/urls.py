from django.urls import path
from .views import GetVersionApiView, github_update_webhook

urlpatterns = [
    path('get-version/', GetVersionApiView.as_view(), name='get-version-api'),
    path("github-update/", github_update_webhook, name="github-update"),
]