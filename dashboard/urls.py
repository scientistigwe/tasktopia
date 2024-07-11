from django.urls import path
from .views import (
    DashboardView,
    UserListView,
    UserDetailView,
    CategoryListView,
    CategoryDetailView,
    TaskListView,
    TaskDetailView,
    task_completion_rate,
    overdue_tasks,
    task_priority_distribution,
    tasks_created_vs_completed,
    productivity_trends,
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
    path('dashboard/', DashboardView.as_view(), name='dashboard'), #okay
     path('overdue-tasks/', overdue_tasks, name='overdue-tasks'),
    path('task-priority-distribution/', task_priority_distribution, name='task-priority-distribution'),#okay
    path('tasks-created-vs-completed/', tasks_created_vs_completed, name='tasks-created-vs-completed'),
    path('productivity-trends/', productivity_trends, name='productivity-trends'),#okay
    path('category-wise-task-completion/', category_wise_task_completion, name='category-wise-task-completion'),#okay
    path('total-tasks/', TotalTasksView.as_view(), name='total_tasks'),#okay
    path('percent-overdue/', PercentOverdueView.as_view(), name='percent-overdue'),#okay
    path('percent-completed/', PercentCompletedView.as_view(), name='percent-completed'),#okay
    path('task-completion-rate-over-time/', task_completion_rate_over_time, name='task_completion_rate_over_time'),
]
