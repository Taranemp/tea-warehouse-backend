from django.urls import path
from .views import TestApiView, github_update_webhook

urlpatterns = [
    path('test/', TestApiView.as_view(), name='test-api'),
    path("github-update/", github_update_webhook, name="github-update"),
]