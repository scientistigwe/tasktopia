from django.urls import path
from .views import (
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    mark_completed,
    update_status,
)

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    # URL for listing tasks

    path('new/', TaskCreateView.as_view(), name='create_task'),
    # URL for creating a new task

    path('<int:pk>/', TaskDetailView.as_view(), name='task_details'),
    # URL for viewing details of a task identified by its primary key

    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='update_task'),
    # URL for updating a task identified by its primary key

    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_confirm_delete'),
    # URL for confirming deletion of a task identified by its primary key

    path('tasks/mark_completed/<int:pk>/', mark_completed, name='mark_completed'),
    # URL endpoint for marking a task as completed via AJAX

    path('tasks/update_status/<int:pk>/', update_status, name='update_status'),
    # URL endpoint for updating the status of a task via AJAX
]
