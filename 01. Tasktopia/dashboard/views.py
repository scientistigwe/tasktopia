# dashboard.views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import UserProfile, Task, Category, Report, Notification, Weather, Forecast, EventLog
from .serializers import UserProfileSerializer, TaskSerializer, CategorySerializer, ReportSerializer, NotificationSerializer, WeatherSerializer, ForecastSerializer, EventLogSerializer
from django.http import HttpRequest, HttpResponse

# Core Views with CRUD operations

# views.py

from rest_framework import generics, permissions
from .models import UserProfile, Task, Category, Report, Notification, Weather, Forecast, EventLog
from .serializers import UserProfileSerializer, TaskSerializer, CategorySerializer, ReportSerializer, NotificationSerializer, WeatherSerializer, ForecastSerializer, EventLogSerializer

# User Profile Views
class UserProfileListView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

# Category Views
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

# Task Views
class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

# Report Views
class ReportListView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

# Notification Views
class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Weather Views
class WeatherListView(generics.ListCreateAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    permission_classes = [permissions.IsAuthenticated]

class WeatherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    permission_classes = [permissions.IsAuthenticated]

# Forecast Views
class ForecastListView(generics.ListCreateAPIView):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    permission_classes = [permissions.IsAuthenticated]

class ForecastDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    permission_classes = [permissions.IsAuthenticated]

# EventLog Views
class EventLogListView(generics.ListCreateAPIView):
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
    permission_classes = [permissions.IsAuthenticated]


# Custom Views for Analysis

@api_view(['GET'])
def dashboard_view(request: HttpRequest) -> HttpResponse:
    # Fetch data for the current user
    tasks = Task.objects.filter(user=request.user)
    completion_rate_response = task_completion_rate(request)
    overdue_tasks_response = overdue_tasks(request)
    priority_distribution_response = task_priority_distribution(request)
    tasks_created_vs_completed_response = tasks_created_vs_completed(request)
    productivity_trends_response = productivity_trends(request)
    category_wise_task_completion_response = category_wise_task_completion(request)

    # Prepare data for rendering in template
    context = {
        'tasks': tasks,
        'completion_rate': completion_rate_response.data['completion_rate'],
        'overdue_tasks': overdue_tasks_response.data,
        'priority_distribution': priority_distribution_response.data,
        'tasks_created_vs_completed': tasks_created_vs_completed_response.data,
        'productivity_trends': productivity_trends_response.data,
        'category_wise_task_completion': category_wise_task_completion_response.data,
    }

    return render(request, 'dashboard.html', context)


@api_view(['GET'])
def task_completion_rate(request):
    """
    Calculate task completion rate for the last 30 days.
    """
    thirty_days_ago = datetime.now() - timedelta(days=30)
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='Completed', updated_at__gte=thirty_days_ago).count()

    if total_tasks > 0:
        completion_rate = (completed_tasks / total_tasks) * 100
    else:
        completion_rate = 0.0

    return Response({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': completion_rate,
    })

@api_view(['GET'])
def overdue_tasks(request):
    """
    Retrieve all overdue tasks.
    """
    overdue_tasks = Task.objects.filter(status='Overdue').order_by('due_date')
    serializer = TaskSerializer(overdue_tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def task_priority_distribution(request):
    """
    Calculate task count distribution by priority.
    """
    priority_distribution = Task.objects.values('priority').annotate(count=Count('id')).order_by('-count')
    return Response(priority_distribution)

@api_view(['GET'])
def tasks_created_vs_completed(request):
    """
    Calculate tasks created vs. completed count for the last 30 days.
    """
    thirty_days_ago = datetime.now() - timedelta(days=30)
    tasks_created = Task.objects.filter(created_at__gte=thirty_days_ago).count()
    tasks_completed = Task.objects.filter(status='Completed', updated_at__gte=thirty_days_ago).count()

    return Response({
        'tasks_created': tasks_created,
        'tasks_completed': tasks_completed,
    })

@api_view(['GET'])
def productivity_trends(request):
    """
    Calculate productivity trends based on tasks created over time.
    """
    thirty_days_ago = datetime.now() - timedelta(days=30)
    productivity_trends = Task.objects.filter(created_at__gte=thirty_days_ago).values('created_at__date').annotate(count=Count('id')).order_by('created_at__date')
    return Response(productivity_trends)

@api_view(['GET'])
def category_wise_task_completion(request):
    """
    Calculate completion rate of tasks by category.
    """
    categories = Category.objects.all()
    category_completion = []
    
    for category in categories:
        total_tasks = Task.objects.filter(category=category).count()
        completed_tasks = Task.objects.filter(category=category, status='Completed').count()

        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
        else:
            completion_rate = 0.0
        
        category_completion.append({
            'category': category.category,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completion_rate
        })
    
    return Response(category_completion)