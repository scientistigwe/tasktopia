from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')  # Adjust 'task_list' to your actual URL name

    def form_valid(self, form):
        # Set the user field to the current user before saving
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_details.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('task_list')  # Adjust 'task_list' to your actual URL name

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')  # Adjust 'task_list' to your actual URL name
