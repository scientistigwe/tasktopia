from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Report, ReportDetail, ReportNotification, UserReport,
    ReportWeather, ReportForecast, ReportEventLog
)
from .serializers import (
    ReportSerializer, ReportDetailSerializer, ReportNotificationSerializer,
    UserReportSerializer, ReportWeatherSerializer, ReportForecastSerializer,
    ReportEventLogSerializer
)
from dashboard.views import (
    task_completion_rate, overdue_tasks, task_priority_distribution,
    tasks_created_vs_completed, productivity_trends, category_wise_task_completion
)
from dashboard.models import Task  # Import Task model from dashboard app

# Report Views
class ReportListView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

# ReportDetail Views
class ReportDetailListView(generics.ListCreateAPIView):
    queryset = ReportDetail.objects.all()
    serializer_class = ReportDetailSerializer
    permission_classes = [IsAuthenticated]

class ReportDetailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportDetail.objects.all()
    serializer_class = ReportDetailSerializer
    permission_classes = [IsAuthenticated]

# ReportNotification Views
class ReportNotificationListView(generics.ListCreateAPIView):
    queryset = ReportNotification.objects.all()
    serializer_class = ReportNotificationSerializer
    permission_classes = [IsAuthenticated]

class ReportNotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportNotification.objects.all()
    serializer_class = ReportNotificationSerializer
    permission_classes = [IsAuthenticated]

# UserReport Views
class UserReportListView(generics.ListCreateAPIView):
    queryset = UserReport.objects.all()
    serializer_class = UserReportSerializer
    permission_classes = [IsAuthenticated]

class UserReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserReport.objects.all()
    serializer_class = UserReportSerializer
    permission_classes = [IsAuthenticated]

# ReportWeather Views
class ReportWeatherListView(generics.ListCreateAPIView):
    queryset = ReportWeather.objects.all()
    serializer_class = ReportWeatherSerializer
    permission_classes = [IsAuthenticated]

class ReportWeatherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportWeather.objects.all()
    serializer_class = ReportWeatherSerializer
    permission_classes = [IsAuthenticated]

# ReportForecast Views
class ReportForecastListView(generics.ListCreateAPIView):
    queryset = ReportForecast.objects.all()
    serializer_class = ReportForecastSerializer
    permission_classes = [IsAuthenticated]

class ReportForecastDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportForecast.objects.all()
    serializer_class = ReportForecastSerializer
    permission_classes = [IsAuthenticated]

# ReportEventLog Views
class ReportEventLogListView(generics.ListCreateAPIView):
    queryset = ReportEventLog.objects.all()
    serializer_class = ReportEventLogSerializer
    permission_classes = [IsAuthenticated]

class ReportEventLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportEventLog.objects.all()
    serializer_class = ReportEventLogSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
def generate_custom_report_view(request):
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')

    if not start_date or not end_date:
        return Response({'error': 'Both start_date and end_date are required.'}, status=400)

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    except ValueError:
        return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    # Fetch data from dashboard views with specified time frame
    completion_rate_response = task_completion_rate(
        None,  # Replace with actual request object or mock
        start_date=start_date,
        end_date=end_date
    )
    overdue_tasks_response = overdue_tasks(
        None,  # Replace with actual request object or mock
        start_date=start_date,
        end_date=end_date
    )
    priority_distribution_response = task_priority_distribution(
        None  # No need for time filtering here
    )
    tasks_created_vs_completed_response = tasks_created_vs_completed(
        None,  # Replace with actual request object or mock
        start_date=start_date,
        end_date=end_date
    )
    productivity_trends_response = productivity_trends(
        None,  # Replace with actual request object or mock
        start_date=start_date,
        end_date=end_date
    )
    category_wise_task_completion_response = category_wise_task_completion(
        None,  # Replace with actual request object or mock
        start_date=start_date,
        end_date=end_date
    )

    # Calculate total number of tasks within the specified time frame
    total_tasks = Task.objects.filter(created_at__gte=start_date, created_at__lte=end_date).count()

    # Aggregate all data into a report structure
    report_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'total_tasks': total_tasks,  # Include total tasks in the report
        'completion_rate': completion_rate_response.data['completion_rate'],
        'overdue_tasks': overdue_tasks_response.data,
        'priority_distribution': priority_distribution_response.data,
        'tasks_created_vs_completed': tasks_created_vs_completed_response.data,
        'productivity_trends': productivity_trends_response.data,
        'category_wise_task_completion': category_wise_task_completion_response.data,
        # Add more custom analysis data as needed
    }

    # Save the report data to the Report model or a suitable storage
    report = Report.objects.create(data=report_data)

    return Response({'message': 'Custom report generated successfully.', 'report_id': report.id})
