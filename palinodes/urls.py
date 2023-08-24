from django.urls import path
from . import views
from .views import CreateRepository

urlpatterns = [
    path('', views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("new-repository", CreateRepository.as_view(), name="new-repository"),
    path("repository/<int:repository_id>", views.repository_view, name="repository"),
    #API urls
    path("directory/<int:pk>", views.directory_api, name="directory"),
    path("new-directory", views.new_directory_api, name="new-directory"),
    #Login urls
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout")
]
