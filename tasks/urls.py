from django.urls import path
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView, mark_completed, update_status

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('new/', TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_details'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='update_task'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_confirm_delete'),
    path('tasks/mark_completed/<int:pk>/', mark_completed, name='mark_completed'),
    path('tasks/update_status/<int:pk>/', update_status, name='update_status'),
]
