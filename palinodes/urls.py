from django.urls import path
from . import views
from . import apis
from .views import CreateRepository

urlpatterns = [
    path('', views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("new-repository", CreateRepository.as_view(), name="new-repository"),
    path("repository/<int:repository_id>", views.repository_view, name="repository"),
    #API urls
    path("notifications", apis.notifications_api, name="notifications"),
    path("directory/<int:pk>", apis.directory_api, name="directory"),
    path("repository/<int:repositorypk>/comments", apis.get_comments_api, name="comments"),
    path("new-directory", apis.new_directory_api, name="new-directory"),
    path("new-file", apis.upload_file_api, name="new-file"),
    path("new-comment", apis.new_comment, name="new-comment"),
    path("delete-directory", apis.delete_directory_api, name="delete-directory"),
    path("delete-file", apis.delete_file_api, name="delete-file"),
    path("remove-collaborator/<int:repositorypk>", apis.remove_collaborator_api, name="remove_collaborator"),
    #Login urls
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout")
]
