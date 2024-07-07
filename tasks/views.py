from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib import messages
from .models import Task, Category
from .forms import TaskForm, CategoryForm

class TaskListView(LoginRequiredMixin, ListView):
    """
    View to list all tasks for the logged-in user.
    """
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        """
        Override to filter tasks by the logged-in user.
        """
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add user and messages to context data.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        # Get the messages from the session and then clear them
        context['success_message'] = self.request.session.pop('success_message', '')
        context['first_name'] = self.request.session.pop('first_name', '')
        context['error_message'] = self.request.session.pop('error_message', '')
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        """
        Process the form and associate the task with the logged-in user.
        """
        form.instance.user = self.request.user

        # Process the category form if valid
        category_form = CategoryForm(self.request.POST)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.user = self.request.user
            category.save()
            form.instance.category = category
            form.instance.save()

        # Set task_success_message in the session for display in the template
        self.request.session['task_success_message'] = 'Task created successfully!'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add category form to context data.
        """
        context = super().get_context_data(**kwargs)
        if 'category_form' not in context:
            context['category_form'] = CategoryForm()
        return context
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update an existing task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        """
        Process the form and handle validation errors.
        """
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            self.object.update_status()
            self.object.save()
            messages.success(self.request, 'Task updated successfully!')
            return response
        except ValidationError as e:
            form.add_error(None, e)
            messages.error(self.request, 'Please correct the errors below.')
            return self.form_invalid(form)

class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    View to display details of a single task.
    """
    model = Task
    template_name = 'tasks/task_details.html'
    context_object_name = 'task'

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete a task.
    """
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def delete(self, request, *args, **kwargs):
        """
        Override to add a success message upon deletion.
        """
        messages.success(self.request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)

@require_POST
@csrf_exempt
def mark_completed(request, pk):
    """
    Marks a task as completed. If the request is via AJAX, returns a JSON response.
    """
    task = get_object_or_404(Task, pk=pk)

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
