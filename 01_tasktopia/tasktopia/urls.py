# tasktopia/urls.py

from django.contrib import admin
from django.urls import path, include
#from dashboard.views import dashboard_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/', include('reports.urls')),
    path('tasks/', include('tasks.urls')),  # Updated path for tasks
    #path('dashboard/', dashboard_view, name='dashboard'),
]
