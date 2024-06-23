# tasktopia/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from dashboard.views import DashboardView 

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('reports/', include('reports.urls')),
    path('tasks/', include('tasks.urls')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/', include('dashboard.urls')),
]
