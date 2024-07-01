from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect

from .models import Task
from .forms import TaskForm

class TaskListView(LoginRequiredMixin, ListView):
    """View to list all tasks for the logged-in user."""
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
    """View to create a new task and assign it to the logged-in user."""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        """Update status after saving"""
        form.instance.user = self.request.user
        response = super().form_valid(form)
        form.instance.update_status()
        return response

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """View to update an existing task and ensure it is assigned to the logged-in user."""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form.valid(form)
        form.instance.update_status()
        return response
    
class TaskDetailView(LoginRequiredMixin, DetailView):
    """View to display details of a specific task."""
    model = Task
    template_name = 'tasks/task_details.html'
    context_object_name = 'task'

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """View to delete a specific task."""
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

class UpdateProgressView(LoginRequiredMixin, View):
    """View to update the progress of a specific task."""

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        progress = request.POST.get('progress')
        if progress is not None:
            task.progress = int(progress)
            task.update_status()
            task.save()
        return redirect('task_details', pk=pk)
