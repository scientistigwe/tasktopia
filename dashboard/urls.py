from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    TaskListView,
    TaskDetailView,
    CategoryListView,
    CategoryDetailView,
    DashboardView,
    task_completion_rate,
    overdue_tasks,
    task_priority_distribution,
    TotalTasksView,
    PercentOverdueView,
    PercentCompletedView,
    productivity_trends,
    category_wise_task_completion_summary,
    tasks_created_vs_completed,
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
    path('task-completion-rate/', task_completion_rate, name='task-completion-rate'),
    path('overdue-tasks/', overdue_tasks, name='overdue-tasks'),
    path('task-priority-distribution/', task_priority_distribution, name='task-priority-distribution'),
    path('tasks-created-vs-completed/', tasks_created_vs_completed, name='tasks-created-vs-completed'),
    path('productivity-trends/', productivity_trends, name='productivity-trends'),
    path('category-wise-task-completion-summary/', category_wise_task_completion_summary, name='category-wise-task-completion-summary'),
    path('total-tasks/', TotalTasksView.as_view(), name='total_tasks'),
    path('percent-overdue/', PercentOverdueView.as_view(), name='percent-overdue'),
    path('percent-completed/', PercentCompletedView.as_view(), name='percent-completed'),
]
