from django.contrib import admin
from django.urls import path
from tasks.views import (
    TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/new/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]
