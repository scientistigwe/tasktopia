from rest_framework import generics, permissions
from django.db.models import Count, Case, When, IntegerField, Sum
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.serializers import UserSerializer, TaskSerializer, CategorySerializer
from django.utils.decorators import method_decorator
from tasks.models import Task, Category

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """
    Render the dashboard.html template.
    """
    template_name = 'dashboard/dashboard.html'

class UserListView(generics.ListCreateAPIView):
    """
    API view to list and create users.
    Only accessible by admin users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete a user.
    Only accessible by admin users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryListView(generics.ListCreateAPIView):
    """
    API view to list and create categories.
    Only accessible by authenticated users.
    Superusers can see all categories, regular users only their own.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Category.objects.all() if user.is_superuser else Category.objects.filter(user=user)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete a category.
    Only accessible by authenticated users.
    Superusers can see all categories, regular users only their own.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Category.objects.all() if user.is_superuser else Category.objects.filter(user=user)

class TaskListView(generics.ListCreateAPIView):
    """
    API view to list and create tasks.
    Only accessible by authenticated users.
    Superusers can see all tasks, regular users only their own.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.all() if user.is_superuser else Task.objects.filter(user=user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete a task.
    Only accessible by authenticated users.
    Superusers can see all tasks, regular users only their own.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.all() if user.is_superuser else Task.objects.filter(user=user)

@login_required
def overdue_tasks(request: HttpRequest) -> JsonResponse:
    try:
        user = request.user
        if user.is_superuser:
            overdue_tasks = Task.objects.filter(status='Overdue').values('user_id', 'title', 'status')
            user_ids = [task['user_id'] for task in overdue_tasks]
            user_details = User.objects.filter(id__in=user_ids).values('id', 'username', 'email', 'first_name')
            user_details_map = {user['id']: user for user in user_details}
            for task in overdue_tasks:
                task['username'] = user_details_map.get(task['user_id'], {}).get('username', '')
                task['email'] = user_details_map.get(task['user_id'], {}).get('email', '')
                task['first_name'] = user_details_map.get(task['user_id'], {}).get('first_name', '')
        else:
            overdue_tasks = Task.objects.filter(user=user, status='Overdue').values('user_id', 'title', 'status')
            for task in overdue_tasks:
                task['username'] = user.username
                task['email'] = user.email
                task['first_name'] = user.first_name

        data = list(overdue_tasks)
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
def task_completion_by_priority_user(request: HttpRequest) -> JsonResponse:
    try:
        if request.user.is_superuser:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(user=request.user)

        task_completion_data = tasks.values('priority', 'user_id').annotate(
            total_tasks=Count('id'),
            completed_tasks=Count(Case(When(status='Completed', then=1))),
            completion_rate=Case(
                When(total_tasks=0, then=0),
                default=(Count(Case(When(status='Completed', then=1))) * 100) / Count('id'),
                output_field=IntegerField()
            )
        )

        return JsonResponse(list(task_completion_data), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def category_wise_task_completion(request: HttpRequest) -> JsonResponse:
    try:
        if request.user.is_superuser:
            categories_queryset = Category.objects.annotate(
                total_tasks=Count('tasks'),
                completed_tasks=Sum(Case(
                    When(tasks__status='Completed', then=1),
                    default=0,
                    output_field=IntegerField()
                )),
            ).values('category_type', 'category_name', 'total_tasks', 'completed_tasks', 'user_id')
        else:
            categories_queryset = Category.objects.filter(user=request.user).annotate(
                total_tasks=Count('tasks'),
                completed_tasks=Sum(Case(
                    When(tasks__status='Completed', then=1),
                    default=0,
                    output_field=IntegerField()
                )),
            ).values('category_type', 'category_name', 'total_tasks', 'completed_tasks', 'user_id')

        categories_list = list(categories_queryset)

        for category in categories_list:
            total_tasks = category['total_tasks']
            completed_tasks = category['completed_tasks']
            category['completion_rate'] = (completed_tasks / total_tasks) * 100.0 if total_tasks > 0 else 0.0

        return JsonResponse(categories_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class TotalTasksView(LoginRequiredMixin, View):
    """
    View to return the total number of tasks for the current user.
    """
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
    """
    View to return the percentage of overdue tasks for the current user.
    """
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
    """
    View to return the percentage of completed tasks for the current user.
    """
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

@login_required
def task_completion_rate_over_time(request: HttpRequest) -> JsonResponse:
    """
    Calculate the task completion rate over the last 30 days.
    """
    try:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        user = request.user
        tasks = Task.objects.filter(user=user, updated_at__gte=thirty_days_ago) if not user.is_superuser else Task.objects.filter(updated_at__gte=thirty_days_ago)

        completion_rate_data = tasks.annotate(
            date=TruncDate('updated_at')
        ).values('date').annotate(
            total_tasks=Count('task_id'),
            completed_tasks=Sum(
                Case(
                    When(status='Completed', then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).order_by('date')

        for entry in completion_rate_data:
            entry['completion_rate'] = (entry['completed_tasks'] / entry['total_tasks']) * 100.0 if entry['total_tasks'] > 0 else 0.0

        return JsonResponse(list(completion_rate_data), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def task_priority_distribution(request: HttpRequest) -> JsonResponse:
    """
    Calculate the task count distribution by priority.
    """
    try:
        user = request.user
        tasks = Task.objects.filter(user=user) if not user.is_superuser else Task.objects.all()

        priority_distribution = tasks.values('priority').annotate(
            count=Count('task_id')
        ).order_by('-count')

        data = list(priority_distribution)

        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)