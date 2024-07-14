from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from .models import Task, Category
from .forms import TaskForm, CategoryForm
from accounts.utils import add_message


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
        context['success_message'] = self.request.session.pop('success_message', '')
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
        Also handles creation of associated category.
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

        # Set success message in the session for display in the template
        self.request.session['success_message'] = 'Task created successfully!'
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Add error message to session and render form again if form is invalid.
        """
        add_message(self.request, 'Error creating task. Please correct the errors.', messages.ERROR)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Add category form to context data.
        """
        context = super().get_context_data(**kwargs)
        if 'category_form' not in context:
            context['category_form'] = CategoryForm()
        return context


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
        Override delete method to add success message upon task deletion.
        """
        messages.success(self.request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update a task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        """
        Add category form to context data for updating task.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['category_form'] = CategoryForm(self.request.POST, instance=self.object.category)
        else:
            context['category_form'] = CategoryForm(instance=self.object.category)
        return context

    def form_valid(self, form):
        """
        Process the form and associated category form upon successful validation.
        """
        category_form = CategoryForm(self.request.POST, instance=self.object.category)
        if category_form.is_valid():
            response = super().form_valid(form)
            category_form.save()
            messages.success(self.request, 'Task updated successfully!')
            return response
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Add error message to request and render form again if form is invalid.
        """
        messages.error(self.request, 'Please correct the errors below.')
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


@require_POST
@csrf_exempt
def mark_completed(request, pk):
    """
    Marks a task as completed. If request is via AJAX, returns JSON response.
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


@require_POST
@csrf_exempt
def update_status(request, pk):
    """
    Updates the status of a task. If request is via AJAX, returns JSON response.
    """
    task = get_object_or_404(Task, pk=pk)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        new_status = request.POST.get('status')
        if new_status:
            try:
                task.status = new_status
                task.save()
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Invalid status'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
