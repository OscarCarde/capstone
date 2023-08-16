from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("repository/<int:repository_id>", views.repository, name="repository"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout")
]
