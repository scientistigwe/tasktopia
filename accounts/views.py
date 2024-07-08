from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import SignupForm
from dashboard.models import Task
from .models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView, View, ListView
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    template_name = 'registration/profile_edit.html'
    success_url = reverse_lazy('profile')
    success_message = "Profile successfully updated."

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, error_message="There was an error updating your profile. Please correct the errors below."))

class DeleteAccountView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.check_password(request.POST['password']):  # Validate password to ensure action is intentional
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid password. Please try again.')
            return redirect('profile')  # Redirect to profile or appropriate page
            
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
                request.session['success_message'] = 'Successfully Signed up.'
                request.session['first_name'] = form.cleaned_data.get('first_name')
                return redirect(reverse('task_list'))
            else:
                request.session['error_message'] = 'There was an error logging you in after signup. Please try logging in manually.'
                return redirect(reverse('login'))
        else:
            request.session['error_message'] = 'There was an error with your signup. Please correct the errors below.'
            return render(request, self.template_name, {'form': form})

class IndexView(TemplateView):
    template_name = 'registration/index.html'

    def get(self, request):
        return render(request, self.template_name)

class LoginView(View):
    """
    Handle user login.

    This view manages the user login process. On a GET request, it renders
    the login form. On a POST request, it processes the login credentials
    and authenticates the user. If the login is successful, it sets a success
    message in the session and redirects the user to the task list page. If
    the login fails, it sets an error message in the session and redirects
    the user back to the login page.
    """
    template_name = 'registration/login.html'

    def get(self, request):
        """Render the login form."""
        return render(request, self.template_name)

    def post(self, request):
        """
        Process login form submission.

        Authenticate the user with the provided username and password.
        If authentication is successful, log the user in, set a success message,
        and redirect to the task list page. If authentication fails, set an
        error message and redirect back to the login page.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['success_message'] = 'Successfully logged in.'
            request.session['first_name'] = user.first_name  # Assuming the user has a first_name attribute
            return redirect(reverse('task_list'))
        else:
            request.session['error_message'] = 'Invalid username or password.'
            return redirect(reverse('index'))
      
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user is not None:
            first_name = request.user.first_name
            logout(request)
            messages.add_message(request, messages.SUCCESS, f'{first_name}, successfully logged out.', extra_tags='logout')
        else:
            # Optionally handle the case where user is None (though it should not normally happen)
            messages.error(request, 'Error: User not logged in.')
        
        return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class TaskListView(ListView):
    model = Task
    template_name = 'registration/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
