from django.urls import path
from . import views

urlpatterns = [
    # Core Views with CRUD operations
    path('user-profiles/', views.UserProfileListView.as_view(), name='userprofile-list'),
    path('user-profiles/<int:pk>/', views.UserProfileDetailView.as_view(), name='userprofile-detail'),

    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    path('reports/', views.ReportListView.as_view(), name='report-list'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),

    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),

    path('weathers/', views.WeatherListView.as_view(), name='weather-list'),
    path('weathers/<int:pk>/', views.WeatherDetailView.as_view(), name='weather-detail'),

    path('forecasts/', views.ForecastListView.as_view(), name='forecast-list'),
    path('forecasts/<int:pk>/', views.ForecastDetailView.as_view(), name='forecast-detail'),

    path('event-logs/', views.EventLogListView.as_view(), name='eventlog-list'),
    path('event-logs/<int:pk>/', views.EventLogDetailView.as_view(), name='eventlog-detail'),

    # Custom Views for Analysis
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/task-completion-rate/', views.task_completion_rate, name='task-completion-rate'),
    path('dashboard/overdue-tasks/', views.overdue_tasks, name='overdue-tasks'),
    path('dashboard/task-priority-distribution/', views.task_priority_distribution, name='task-priority-distribution'),
    path('dashboard/tasks-created-vs-completed/', views.tasks_created_vs_completed, name='tasks-created-vs-completed'),
    path('dashboard/productivity-trends/', views.productivity_trends, name='productivity-trends'),
    path('dashboard/category-wise-task-completion/', views.category_wise_task_completion, name='category-wise-task-completion'),
]
