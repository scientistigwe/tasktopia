from django.urls import path
from .views import (
    DashboardView,
    UserListView,
    UserDetailView,
    CategoryListView,
    CategoryDetailView,
    TaskListView,
    TaskDetailView,
    overdue_tasks,
    task_priority_distribution,
    tasks_created_vs_completed,
    task_completion_by_priority_user,
    category_wise_task_completion,
    TotalTasksView,
    PercentOverdueView,
    PercentCompletedView,
    task_completion_rate_over_time,
    )

urlpatterns = [
    # User URLs
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Dashboard URLs
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 
     path('overdue-tasks/', overdue_tasks, name='overdue-tasks'),
    path('task-priority-distribution/', task_priority_distribution, name='task-priority-distribution'),
    path('tasks-created-vs-completed/', tasks_created_vs_completed, name='tasks-created-vs-completed'),
    path('task-completion-by-priority-user/', task_completion_by_priority_user, name='task-completion-by-priority-user'),
    path('category-wise-task-completion/', category_wise_task_completion, name='category-wise-task-completion'),
    path('total-tasks/', TotalTasksView.as_view(), name='total_tasks'),
    path('percent-overdue/', PercentOverdueView.as_view(), name='percent-overdue'),
    path('percent-completed/', PercentCompletedView.as_view(), name='percent-completed'),
    path('task-completion-rate-over-time/', task_completion_rate_over_time, name='task_completion_rate_over_time'),
]
