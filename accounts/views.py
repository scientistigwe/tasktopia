# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import SignupForm, CustomUserChangeForm
from dashboard.models import Task
from django.views.generic import TemplateView, UpdateView, View, ListView
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .utils import add_message
from django.contrib import messages

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'registration/profile_edit.html'
    success_url = reverse_lazy('task_list')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile. Please correct the errors.')
        return super().form_invalid(form)
    
class DeleteAccountView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/delete_account.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.POST.get('password')
        
        # Authenticate the user
        if user.check_password(password):
            # Password is correct, proceed with account deletion
            username = user.username
            user.delete()
            messages.success(request, f'Your account ({username}) has been deleted.')
            return redirect('index')
        else:
            # Password is incorrect
            messages.error(request, 'Incorrect password. Account not deleted.')
            return redirect('delete_account')
        
class SignupView(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                add_message(request, 'Successfully signed up.', messages.SUCCESS)
                request.session['first_name'] = form.cleaned_data.get('first_name')
                return redirect('task_list')
        else:
            request.session['error_message'] = 'There was an error with your signup. Please correct the errors below.'
            return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            add_message(request, 'Successfully logged in.', messages.SUCCESS)
            return redirect('task_list')
        
        add_message(request, 'Invalid credentials.', messages.ERROR)
        return redirect('login')

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            first_name = request.user.first_name
            logout(request)
            add_message(request, f'{first_name}, you have successfully logged out.', messages.SUCCESS)
        return redirect('index')

class IndexView(TemplateView):
    template_name = 'registration/index.html'

class ClearMessageView(View):
    def post(self, request):
        message_key = request.POST.get('message_key')
        if message_key in request.session:
            del request.session[message_key]
        return JsonResponse({'status': 'success'})
