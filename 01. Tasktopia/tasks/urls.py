from django.urls import path
from . import views

urlpatterns = [
    # Django Views
    path('', views.TaskListView.as_view(), name='task-list'),
    path('create/', views.TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),

    # REST Framework API Views
    path('api/tasks/', views.TaskListAPIView.as_view(), name='task-list-api'),
    path('api/tasks/<int:pk>/', views.TaskDetailAPIView.as_view(), name='task-detail-api'),

    path('api/usertasks/', views.UserTaskListAPIView.as_view(), name='usertask-list-api'),
    path('api/usertasks/<int:pk>/', views.UserTaskDetailAPIView.as_view(), name='usertask-detail-api'),

    path('api/taskcategories/', views.TaskCategoryListAPIView.as_view(), name='taskcategory-list-api'),
    path('api/taskcategories/<int:pk>/', views.TaskCategoryDetailAPIView.as_view(), name='taskcategory-detail-api'),

    path('api/taskweather/', views.TaskWeatherListAPIView.as_view(), name='taskweather-list-api'),
    path('api/taskweather/<int:pk>/', views.TaskWeatherDetailAPIView.as_view(), name='taskweather-detail-api'),

    path('api/taskforecast/', views.TaskForecastListAPIView.as_view(), name='taskforecast-list-api'),
    path('api/taskforecast/<int:pk>/', views.TaskForecastDetailAPIView.as_view(), name='taskforecast-detail-api'),

    path('api/taskreport/', views.TaskReportListAPIView.as_view(), name='taskreport-list-api'),
    path('api/taskreport/<int:pk>/', views.TaskReportDetailAPIView.as_view(), name='taskreport-detail-api'),
]
