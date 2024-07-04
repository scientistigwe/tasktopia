# Import all necessary libraries
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from dashboard.models import Task
from .forms import TaskForm, MarkTaskAsCompletedForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# 
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            self.object.update_status()
            self.object.save()
            return response
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            self.object.update_status()
            self.object.save()
            return response
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Description:

    Args:

    Return:
    """
    model = Task
    template_name = 'tasks/task_details.html'
    context_object_name = 'task'

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

@require_POST
@csrf_exempt
def mark_completed(request, pk):
    """
    Marks a task as completed. If the request is via AJAX, returns a JSON response.
    """
    task = get_object_or_404(Task, pk=pk)

    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            task.is_manually_completed = True
            task.status = Task.Status.COMPLETED
            task.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
