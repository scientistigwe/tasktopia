# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from dashboard.models import Task

class IndexView(View):
    def get(self, request):
        return render(request, 'registration/index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')  # Assuming 'index' is the name of your index page

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class TaskListView(ListView):
    model = Task
    template_name = 'registration/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    @login_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
