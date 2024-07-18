# Django imports
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

# Application-specific imports
from dashboard.views import DashboardView 
from django.conf import settings
from django.conf.urls.static import static

# Module-level comments for the urlpatterns list
urlpatterns = [
    # Homepage URL
    path('', TemplateView.as_view(template_name='registration/index.html'), name='home'),

    # Admin URL
    path('admin/', admin.site.urls),

    # Accounts URLs (including authentication URLs)
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # Tasks URLs
    path('tasks/', include('tasks.urls')),

    # Dashboard URL
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/', include('dashboard.urls')),  # Include additional dashboard URLs here

]