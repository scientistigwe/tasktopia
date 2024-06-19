# urls.py

from django.urls import path
from .views import (
    UserProfileListView,
    UserProfileDetailView,
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
    dashboard_view,
    task_completion_rate,
    overdue_tasks,
    task_priority_distribution,
    tasks_created_vs_completed,
    productivity_trends,
    category_wise_task_completion,
)

urlpatterns = [
    # User Profile URLs
    path('user-profiles/', UserProfileListView.as_view(), name='userprofile-list'),
    path('user-profiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),

    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Report URLs
    path('reports/', ReportListView.as_view(), name='report-list'),
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
    path('event-logs/', EventLogListView.as_view(), name='eventlog-list'),
    path('event-logs/<int:pk>/', EventLogDetailView.as_view(), name='eventlog-detail'),

    # Dashboard URLs
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/task-completion-rate/', task_completion_rate, name='task-completion-rate'),
    path('dashboard/overdue-tasks/', overdue_tasks, name='overdue-tasks'),
    path('dashboard/task-priority-distribution/', task_priority_distribution, name='task-priority-distribution'),
    path('dashboard/tasks-created-vs-completed/', tasks_created_vs_completed, name='tasks-created-vs-completed'),
    path('dashboard/productivity-trends/', productivity_trends, name='productivity-trends'),
    path('dashboard/category-wise-task-completion/', category_wise_task_completion, name='category-wise-task-completion'),
]
