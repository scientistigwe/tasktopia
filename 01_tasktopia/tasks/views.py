from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from.models import TaskRelationship
from.forms import TaskForm
from accounts.models import User

class UserFilterMixin:
    """
    Mixin to filter queryset based on the current user.
    """
    def get_queryset(self):
        return TaskRelationship.objects.filter(user=self.request.user)

class TaskListView(LoginRequiredMixin, ListView, UserFilterMixin):
    model = TaskRelationship
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

class TaskCreateView(LoginRequiredMixin, CreateView, UserFilterMixin):
    model = TaskRelationship
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        task_relationship = form.save(commit=False)
        task_relationship.user = self.request.user
        task_relationship.save()
        return super().form_valid(form)

class TaskDetailView(LoginRequiredMixin, DetailView, UserFilterMixin):
    model = TaskRelationship
    template_name = 'tasks/task_details.html'
    context_object_name = 'task'

class TaskUpdateView(LoginRequiredMixin, UpdateView, UserFilterMixin):
    model = TaskRelationship
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(LoginRequiredMixin, DeleteView, UserFilterMixin):
    model = TaskRelationship
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
