from django.urls import path
from . import views

urlpatterns = [
    # Report Views
    path('reports/', views.ReportListView.as_view(), name='report-list'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),

    # ReportDetail Views
    path('report-details/', views.ReportDetailListView.as_view(), name='reportdetail-list'),
    path('report-details/<int:pk>/', views.ReportDetailDetailView.as_view(), name='reportdetail-detail'),

    # ReportNotification Views
    path('report-notifications/', views.ReportNotificationListView.as_view(), name='reportnotification-list'),
    path('report-notifications/<int:pk>/', views.ReportNotificationDetailView.as_view(), name='reportnotification-detail'),

    # UserReport Views
    path('user-reports/', views.UserReportListView.as_view(), name='userreport-list'),
    path('user-reports/<int:pk>/', views.UserReportDetailView.as_view(), name='userreport-detail'),

    # ReportWeather Views
    path('report-weathers/', views.ReportWeatherListView.as_view(), name='reportweather-list'),
    path('report-weathers/<int:pk>/', views.ReportWeatherDetailView.as_view(), name='reportweather-detail'),

    # ReportForecast Views
    path('report-forecasts/', views.ReportForecastListView.as_view(), name='reportforecast-list'),
    path('report-forecasts/<int:pk>/', views.ReportForecastDetailView.as_view(), name='reportforecast-detail'),

    # ReportEventLog Views
    path('report-eventlogs/', views.ReportEventLogListView.as_view(), name='reporteventlog-list'),
    path('report-eventlogs/<int:pk>/', views.ReportEventLogDetailView.as_view(), name='reporteventlog-detail'),

    # Custom Report Generation API
    path('generate-custom-report/', views.generate_custom_report_view, name='generate-custom-report'),
]
