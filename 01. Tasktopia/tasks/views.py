from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from rest_framework import generics
from .models import Task, UserTask, TaskCategory, TaskWeather, TaskForecast, TaskReport
from .serializers import (
    TaskSerializer, UserTaskSerializer, TaskCategorySerializer,
    TaskWeatherSerializer, TaskForecastSerializer, TaskReportSerializer
)

# Django Views
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'  # Replace with your template
    context_object_name = 'tasks'  # Context variable name in template

class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/task_form.html'  # Replace with your template
    fields = '__all__'  # Specify fields or exclude as needed

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'  # Replace with your template
    context_object_name = 'task'  # Context variable name in template

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'  # Replace with your template
    fields = '__all__'  # Specify fields or exclude as needed

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'  # Replace with your template
    success_url = '/tasks/'  # URL to redirect after successful delete

# REST Framework API Views
class TaskListAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserTaskListAPIView(generics.ListCreateAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer

class UserTaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer

class TaskCategoryListAPIView(generics.ListCreateAPIView):
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer

class TaskCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer

class TaskWeatherListAPIView(generics.ListCreateAPIView):
    queryset = TaskWeather.objects.all()
    serializer_class = TaskWeatherSerializer

class TaskWeatherDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskWeather.objects.all()
    serializer_class = TaskWeatherSerializer

class TaskForecastListAPIView(generics.ListCreateAPIView):
    queryset = TaskForecast.objects.all()
    serializer_class = TaskForecastSerializer

class TaskForecastDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskForecast.objects.all()
    serializer_class = TaskForecastSerializer

class TaskReportListAPIView(generics.ListCreateAPIView):
    queryset = TaskReport.objects.all()
    serializer_class = TaskReportSerializer

class TaskReportDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskReport.objects.all()
    serializer_class = TaskReportSerializer
