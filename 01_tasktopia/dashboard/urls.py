from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    TaskListView,
    TaskDetailView,
    CategoryListView,
    CategoryDetailView,
    ReportListView,
    ReportDetailView,
    NotificationListView,
    NotificationDetailView,
    WeatherListView,
    WeatherDetailView,
    ForecastListView,
    ForecastDetailView,
    EventLogListView,
    EventLogDetailView,
    DashboardView,
    task_completion_rate,
    overdue_tasks,
    task_priority_distribution,
    TotalTasksView,
    PercentOverdueView,
    PercentCompletedView,
    productivity_trends,
    category_wise_task_completion,
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

    # Report URLs
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),

    # Notification URLs
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),

    # Weather URLs
    path('weathers/', WeatherListView.as_view(), name='weather-list'),
    path('weathers/<int:pk>/', WeatherDetailView.as_view(), name='weather-detail'),

    # Forecast URLs
    path('forecasts/', ForecastListView.as_view(), name='forecast-list'),
    path('forecasts/<int:pk>/', ForecastDetailView.as_view(), name='forecast-detail'),

    # EventLog URLs
    path('event-logs/', EventLogListView.as_view(), name='event-log-list'),
    path('event-logs/<int:pk>/', EventLogDetailView.as_view(), name='event-log-detail'),

    # Dashboard URLs
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('task-completion-rate/', task_completion_rate, name='task-completion-rate'),
    path('overdue-tasks/', overdue_tasks, name='overdue-tasks'),
    path('task-priority-distribution/', task_priority_distribution, name='task-priority-distribution'),
    path('tasks-created-vs-completed/', tasks_created_vs_completed, name='tasks-created-vs-completed'),
    path('productivity-trends/', productivity_trends, name='productivity-trends'),
    path('category-wise-task-completion/', category_wise_task_completion, name='category-wise-task-completion'),
    path('total-tasks/', TotalTasksView.as_view(), name='total_tasks'),
    path('percent-overdue/', PercentOverdueView.as_view(), name='percent-overdue'),
    path('percent-completed/', PercentCompletedView.as_view(), name='percent-completed'),
]
