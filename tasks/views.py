from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Task
from .forms import TaskForm

class TaskListView(LoginRequiredMixin, ListView):
    """
    View to list all tasks for the logged-in user.
    """
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        """
        Filter tasks to show only those belonging to the logged-in user.
        """
        return Task.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """
        Add the current user to the context data.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new task and assign it to the logged-in user.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        """
        Assign the task to the current user and update its status before saving.
        """
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
    """
    View to update an existing task and ensure it is assigned to the logged-in user.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        """
        Ensure the task is assigned to the current user and update its status before saving.
        """
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
    View to display details of a specific task.
    """
    model = Task
    template_name = 'tasks/task_details.html'
    context_object_name = 'task'

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete a specific task.
    """
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
@require_POST
def mark_completed(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        if 'completed' in request.POST:
            task.status = 'Completed'
            task.save()
        return redirect('task_list')
    except Task.DoesNotExist:
        return redirect('task_list')