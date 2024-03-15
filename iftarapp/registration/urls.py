
from registration import views
from django.urls import path
from . import views
urlpatterns = [
    path("registration", views.registration, name="registration"),
    path("authn", views.superuser, name="authentication"),
    path("admin", views.admin, name="superuser"),
    path("access_denied", views.access_denied, name="access_denied")
]