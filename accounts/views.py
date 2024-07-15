"""
Views for user authentication and profile management.
"""

# Import necessary modules and functions from Django and the project
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, CustomUserChangeForm
from django.views.generic import TemplateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from utils import add_message
from django.contrib import messages

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Display the user's profile page.
    Only accessible if the user is logged in.
    """
    template_name = 'registration/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Allow the user to edit their profile information.
    Only accessible if the user is logged in.
    """
    form_class = CustomUserChangeForm
    template_name = 'registration/profile_edit.html'
    success_url = reverse_lazy('task_list')

    def get_object(self):
        """
        Get the current user object.
        """
        return self.request.user

    def form_valid(self, form):
        """
        Handle a valid form submission.
        Display a success message and proceed with the default behavior.
        """
        messages.success(self.request, "Profile successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle an invalid form submission.
        Display an error message and proceed with the default behavior.
        """
        messages.error(self.request, 'Error updating profile. Please correct the errors.')
        return super().form_invalid(form)
    
class DeleteAccountView(LoginRequiredMixin, View):
    """
    Handle account deletion requests.
    Only accessible if the user is logged in.
    """
    def get(self, request, *args, **kwargs):
        """
        Display the account deletion confirmation page.
        """
        return render(request, 'registration/delete_account.html')

    def post(self, request, *args, **kwargs):
        """
        Process the account deletion form submission.
        Delete the account if the provided password is correct.
        """
        user = request.user
        password = request.POST.get('password')
        
        # Authenticate the user
        if user.check_password(password):
            # Password is correct, proceed with account deletion
            username = user.username
            user.delete()
            messages.success(request, f'Your account ({username}) has been deleted.')
            return redirect('index')
        
        # Password is incorrect
        messages.error(request, 'Incorrect password. Account not deleted.')
        return redirect('delete_account')
        
class SignupView(View):
    """
    Handle user sign-up requests.
    """
    template_name = 'registration/signup.html'

    def get(self, request):
        """
        Display the sign-up form.
        """
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Process the sign-up form submission.
        Create a new user if the form is valid.
        """
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                add_message(request, 'Successfully signed up.', messages.SUCCESS)
                request.session['first_name'] = form.cleaned_data.get('first_name')
                return redirect('task_list')
        
        request.session['error_message'] = 'There was an error with your signup. Please correct the errors below.'
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    """
    Handle user login requests.
    """
    template_name = 'registration/login.html'

    def get(self, request):
        """
        Display the login form.
        """
        return render(request, self.template_name)

    def post(self, request):
        """
        Process the login form submission.
        Authenticate and log the user in if the credentials are correct.
        """
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
    """
    Handle user logout requests.
    Only accessible if the user is logged in.
    """
    def get(self, request):
        """
        Log the user out and display a success message.
        """
        if request.user.is_authenticated:
            first_name = request.user.first_name
            logout(request)
            add_message(request, f'{first_name}, you have successfully logged out.', messages.SUCCESS)
        return redirect('index')

class IndexView(TemplateView):
    """
    Display the index page.
    """
    template_name = 'registration/index.html'

class ClearMessageView(View):
    """
    Handle requests to clear a specific session message.
    """
    def post(self, request):
        """
        Clear the specified message from the session.
        """
        message_key = request.POST.get('message_key')
        if message_key in request.session:
            del request.session[message_key]
        return JsonResponse({'status': 'success'})
