from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Task

# Django Views - All use the same template
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/create-task.html'
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'list'
        return context

class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/create-task.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'create'
        return context

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/create-task.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'detail'
        return context

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'tasks/create-task.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'update'
        return context

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/create-task.html'
    success_url = '/tasks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'delete'
        return context
