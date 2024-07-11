from rest_framework import generics, permissions
from django.db.models import Count, Case, When, IntegerField, Sum, F
from datetime import datetime, timedelta
from django.utils import timezone  # Import timezone from django.utils
from django.db.models.functions import TruncDate  # Import TruncDate from django.db.models.functions
from tasks.models import Task, Category
from .serializers import UserSerializer, TaskSerializer, CategorySerializer
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
        return Category.objects.all() if user.is_superuser else Category.objects.filter(user=user)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Category.objects.all() if user.is_superuser else Category.objects.filter(user=user)

# Task Views
class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.all() if user.is_superuser else Task.objects.filter(user=user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.all() if user.is_superuser else Task.objects.filter(user=user)

# Custom Views for Analysis
@login_required
def task_completion_rate(request: HttpRequest) -> JsonResponse:
    """
    Calculate task completion rate for the last 30 days.
    """
    try:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        if request.user.is_superuser:
            total_tasks = Task.objects.count()
            completed_tasks = Task.objects.filter(status='Completed', updated_at__gte=thirty_days_ago).count()
        else:
            total_tasks = Task.objects.filter(user=request.user).count()
            completed_tasks = Task.objects.filter(user=request.user, status='Completed', updated_at__gte=thirty_days_ago).count()

        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0.0

        data = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completion_rate,
        }

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def overdue_tasks(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all overdue tasks.
    """
    try:
        overdue_tasks = Task.objects.filter(user=request.user, status='Overdue').order_by('due_date')
        serialized_data = TaskSerializer(overdue_tasks, many=True).data
        return JsonResponse(serialized_data, safe=False)  # Set safe=False for non-dict objects
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def task_priority_distribution(request: HttpRequest) -> JsonResponse:
    """
    Calculate task count distribution by priority.
    """
    try:
        if request.user.is_superuser:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(user=request.user)

        priority_distribution = tasks.values('priority').annotate(count=Count('id')).order_by('-count')
        data = list(priority_distribution)

        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def tasks_created_vs_completed(request: HttpRequest) -> JsonResponse:
    """
    Calculate tasks created vs. completed count for the last 30 days.
    """
    try:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        if request.user.is_superuser:
            tasks = Task.objects.filter(created_at__gte=thirty_days_ago)
        else:
            tasks = Task.objects.filter(user=request.user, created_at__gte=thirty_days_ago)

        tasks_created = tasks.count()
        tasks_completed = tasks.filter(status='Completed').count()

        data = {
            'tasks_created': tasks_created,
            'tasks_completed': tasks_completed,
        }

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def productivity_trends(request: HttpRequest) -> JsonResponse:
    """
    Calculate productivity trends based on tasks created over time.
    """
    try:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        if request.user.is_superuser:
            tasks = Task.objects.filter(created_at__gte=thirty_days_ago)
        else:
            tasks = Task.objects.filter(user=request.user, created_at__gte=thirty_days_ago)

        productivity_trends = tasks.annotate(
            created_date=TruncDate('created_at')
        ).values('created_date').annotate(count=Count('id')).order_by('created_date')

        return JsonResponse(list(productivity_trends), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def category_wise_task_completion(request: HttpRequest) -> JsonResponse:
    """
    Calculate aggregated completion rate of tasks by category.
    """
    try:
        if request.user.is_superuser:
            categories_queryset = Category.objects.annotate(
                total_tasks=Count('tasks'),
                completed_tasks=Sum(Case(
                    When(tasks__status='Completed', then=1),
                    default=0,
                    output_field=IntegerField()
                )),
            ).values('category_type', 'category_name', 'total_tasks', 'completed_tasks')
        else:
            categories_queryset = Category.objects.filter(user=request.user).annotate(
                total_tasks=Count('tasks'),
                completed_tasks=Sum(Case(
                    When(tasks__status='Completed', then=1),
                    default=0,
                    output_field=IntegerField()
                )),
            ).values('category_type', 'category_name', 'total_tasks', 'completed_tasks')

        categories_list = list(categories_queryset)

        for category in categories_list:
            total_tasks = category['total_tasks']
            completed_tasks = category['completed_tasks']
            category['completion_rate'] = (completed_tasks / total_tasks) * 100.0 if total_tasks > 0 else 0.0

        return JsonResponse(categories_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# KPI Views
class TotalTasksView(LoginRequiredMixin, View):
    def get_queryset(self):
        user = self.request.user
        return Task.objects.all() if user.is_superuser else Task.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        try:
            total_tasks = self.get_queryset().count()
            return JsonResponse({'total_tasks': total_tasks})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class PercentOverdueView(LoginRequiredMixin, View):
    def get_queryset(self):
        user = self.request.user
        return Task.objects.all() if user.is_superuser else Task.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        try:
            tasks = self.get_queryset()
            total_tasks = tasks.count()
            overdue_tasks = tasks.filter(status='Overdue').count()
            percent_overdue = (overdue_tasks / total_tasks) * 100.0 if total_tasks > 0 else 0.0

            return JsonResponse({'percent_overdue': percent_overdue})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class PercentCompletedView(LoginRequiredMixin, View):
    def get_queryset(self):
        user = self.request.user
        return Task.objects.all() if user.is_superuser else Task.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        try:
            tasks = self.get_queryset()
            total_tasks = tasks.count()
            completed_tasks = tasks.filter(status='Completed').count()
            percent_completed = (completed_tasks / total_tasks) * 100.0 if total_tasks > 0 else 0.0

            return JsonResponse({'percent_completed': percent_completed})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
