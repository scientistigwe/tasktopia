from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import SignupForm
from dashboard.models import Task
from .models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView, View, ListView
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    template_name = 'registration/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

class DeleteAccountView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return redirect('index')
    
class SignupView(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            self._create_and_login_user(request, form)
            return redirect('task_list')
        return render(request, self.template_name, {'form': form})

    def _create_and_login_user(self, request, form):
        user = form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        if user is not None:
            login(request, user)

class IndexView(TemplateView):
    template_name = 'registration/index.html'

class LoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')  # Redirect to task list after login
        return render(request, self.template_name, {'error': 'Invalid username or password.'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')  # Redirect to base URL after logout

@method_decorator(login_required, name='dispatch')
class TaskListView(ListView):
    model = Task
    template_name = 'registration/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
