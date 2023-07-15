from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path("", views.StatusesListView.as_view(), name="statuses_list"),
    path("create/", views.CreateStatus.as_view(), name="status_create"),
    path("<int:pk>/update/", views.UpdateStatus.as_view(), name="status_update"),
    path("<int:pk>/delete/", views.DeleteStatus.as_view(), name="status_delete"),
]
