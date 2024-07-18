"""
URL configuration for user authentication and profile management.
"""

from django.contrib.auth import views as auth_views
from django.urls import path
from accounts import views


# URL patterns for the application
urlpatterns = [
    # Index URL
    path('', views.IndexView.as_view(), name='index'),

    # Login, Signup, and Profile URLs
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),

    # Password management URLs
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html'
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # Account management URLs
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete_account'),   
]
