from django.urls import path, include
from task_manager.users import views


urlpatterns = [
    path("", views.ListUsersView.as_view(), name="users_list"),
    path("create/", views.UserFormCreateView.as_view(), name="users_create"),
]
