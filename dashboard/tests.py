from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from tasks.models import Task


class TaskViewsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.task = Task.objects.create(title='Sample Task', description='Sample description', due_date='2024-06-30', priority='High', status='Pending', category_id=1, user_id=1)

    def test_task_list_view(self):
        url = reverse('task-list')  # Replace with your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one task is created

    def test_task_completion_rate_view(self):
        url = reverse('task-completion-rate')  # Replace with your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('completion_rate', response.data)
        completion_rate = response.data['completion_rate']
        self.assertIsInstance(completion_rate, float)  # Ensure completion_rate is of expected type

    def test_task_create_view(self):
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'due_date': '2024-07-01',
            'priority': 'Medium',
            'status': 'Pending',
            'category_id': 1,
            'user_id': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)  # Check that task count increased

    def test_task_update_view(self):
        url = reverse('task-detail', args=[self.task.id])  # Assuming task detail URL is task-detail/<pk> where pk is task id
        data = {'priority': 'Low'}  # Update priority to Low
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()  # Refresh task instance from database
        self.assertEqual(self.task.priority, 'Low')

    def test_task_delete_view(self):
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
