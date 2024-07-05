from rest_framework import generics, permissions
from django.db.models import Count
from datetime import datetime, timedelta
from .models import Task, Category
from .serializers import UserSerializer, TaskSerializer, CategorySerializer
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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

# Custom Views for Analysis
@login_required
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

@login_required
def overdue_tasks(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all overdue tasks.
    """
    overdue_tasks = Task.objects.filter(user=request.user, status='Overdue').order_by('due_date')
    serialized_data = TaskSerializer(overdue_tasks, many=True).data
    return JsonResponse(serialized_data, safe=False)  # Set safe=False for non-dict objects

@login_required
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

@login_required
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

@login_required
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

@login_required
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