from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Task, Category, Report, Notification, Weather, Forecast, EventLog
from .serializers import UserSerializer, TaskSerializer, CategorySerializer, ReportSerializer, NotificationSerializer, WeatherSerializer, ForecastSerializer, EventLogSerializer
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

# View to render dashboard.html
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

# User Views
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# Category Views
class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Category.objects.all()
        return Category.objects.filter(user=user)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Category.objects.all()
        return Category.objects.filter(user=user)

# Task Views
class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=user)

# Report Views
class ReportListView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Report.objects.all()
        return Report.objects.filter(user=user)

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Report.objects.all()
        return Report.objects.filter(user=user)

# Notification Views
class NotificationListView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Notification.objects.all()
        return Notification.objects.filter(user=user)

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Notification.objects.all()
        return Notification.objects.filter(user=user)

# Weather Views
class WeatherListView(generics.ListCreateAPIView):
    serializer_class = WeatherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Weather.objects.all()
        return Weather.objects.filter(user=user)

class WeatherDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WeatherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Weather.objects.all()
        return Weather.objects.filter(user=user)

# Forecast Views
class ForecastListView(generics.ListCreateAPIView):
    serializer_class = ForecastSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Forecast.objects.all()
        return Forecast.objects.filter(user=user)

class ForecastDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ForecastSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Forecast.objects.all()
        return Forecast.objects.filter(user=user)

# EventLog Views
class EventLogListView(generics.ListCreateAPIView):
    serializer_class = EventLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return EventLog.objects.all()
        return EventLog.objects.filter(user=user)

class EventLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return EventLog.objects.all()
        return EventLog.objects.filter(user=user)

# Custom Views for Analysis
def task_completion_rate(request: HttpRequest) -> JsonResponse:
    """
    Calculate task completion rate for the last 30 days.
    """
    thirty_days_ago = datetime.now() - timedelta(days=30)
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, status='Completed', updated_at__gte=thirty_days_ago).count()

    if total_tasks > 0:
        completion_rate = (completed_tasks / total_tasks) * 100
    else:
        completion_rate = 0.0

    data = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': completion_rate,
    }

    return JsonResponse(data)

def overdue_tasks(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all overdue tasks.
    """
    overdue_tasks = Task.objects.filter(user=request.user, status='Overdue').order_by('due_date')
    serialized_data = TaskSerializer(overdue_tasks, many=True).data
    return JsonResponse(serialized_data, safe=False)  # Set safe=False for non-dict objects

def task_priority_distribution(request: HttpRequest) -> JsonResponse:
    """
    Calculate task count distribution by priority.
    """
    tasks = Task.objects.filter(user=request.user)
    if request.user.is_superuser:
        tasks = Task.objects.all()
    
    priority_distribution = tasks.values('priority').annotate(count=Count('task_id')).order_by('-count')
    data = list(priority_distribution)

    return JsonResponse(data, safe=False)  # Set safe=False for non-dict objects

def tasks_created_vs_completed(request: HttpRequest) -> JsonResponse:
    """
    Calculate tasks created vs. completed count for the last 30 days.
    """
    thirty_days_ago = datetime.now() - timedelta(days=30)
    tasks = Task.objects.filter(user=request.user, created_at__gte=thirty_days_ago)
    if request.user.is_superuser:
        tasks = Task.objects.filter(created_at__gte=thirty_days_ago)
    
    tasks_created = tasks.count()
    tasks_completed = tasks.filter(status='Completed').count()

    data = {
        'tasks_created': tasks_created,
        'tasks_completed': tasks_completed,
    }

    return JsonResponse(data)

def productivity_trends(request: HttpRequest) -> JsonResponse:
    """
     Calculate productivity trends based on tasks created over time.
    """
   
    thirty_days_ago = datetime.now() - timedelta(days=30)
    tasks = Task.objects.filter(user=request.user, created_at__gte=thirty_days_ago)
    if request.user.is_superuser:
        tasks = Task.objects.filter(created_at__gte=thirty_days_ago)
    
    productivity_trends = tasks.values('created_at__date').annotate(count=Count('task_id')).order_by('created_at__date')
    return JsonResponse(list(productivity_trends), safe=False)

def category_wise_task_completion(request):
    """
    Calculate completion rate of tasks by category.
    """
    categories = Category.objects.filter(user=request.user)
    if request.user.is_superuser:
        categories = Category.objects.all()

    category_completion = []

    for category in categories:
        if request.user.is_superuser:
            tasks = Task.objects.filter(category=category)
        else:
            tasks = Task.objects.filter(user=request.user, category=category)
        
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()

        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
        else:
            completion_rate = 0.0

        category_completion.append({
            'category': category.category_name,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completion_rate
        })

    return JsonResponse(category_completion, safe=False)

class TotalTasksView(LoginRequiredMixin, View):
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=user)
    
    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        total_tasks = tasks.count()
        return JsonResponse({'total_tasks': total_tasks})

class PercentOverdueView(LoginRequiredMixin, View):

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        total_tasks = tasks.count()
        overdue_tasks = tasks.filter(status='Overdue').count()

        if total_tasks == 0:
            percent_overdue = 0.0  # Ensure percent_overdue is a float
        else:
            percent_overdue = (overdue_tasks / total_tasks) * 100.0  # Ensure division result is float

        return JsonResponse({'percent_overdue': percent_overdue})

class PercentCompletedView(LoginRequiredMixin, View):

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()

        if total_tasks == 0:
            percent_completed = 0.0  # Ensure percent_completed is a float
        else:
            percent_completed = (completed_tasks / total_tasks) * 100.0  # Ensure division result is float

        return JsonResponse({'percent_completed': percent_completed})