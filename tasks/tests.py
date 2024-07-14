from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Category
from .forms import TaskForm, CategoryForm

class TaskTestCase(TestCase):
    """
    TestCase class for testing Task and related views and forms.
    """
    def setUp(self):
        """
        Set up test data for the test methods.
        Creates a user, category, and a task instance.
        """
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(category_name='Test Category', category_type=Category.CategoryType.PERSONAL, user=self.user)
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            start_date='2024-07-15 10:00:00',
            due_date='2024-07-16 12:00:00',
            priority=Task.Priority.HIGH,
            status=Task.Status.PENDING,
            category=self.category,
            user=self.user
        )

    def test_task_list_view(self):
        """
        Test the task list view to ensure it returns the correct tasks for the logged-in user.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['tasks'], ['<Task: Title: Test Task, Priority: High, Status: Pending>'])

    def test_task_detail_view(self):
        """
        Test the task detail view to ensure it returns the correct task details for the given task.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('task_details', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'].title, 'Test Task')

    def test_task_create_view(self):
        """
        Test the task create view to ensure a new task is created successfully.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('create_task'), {
            'title': 'New Test Task',
            'description': 'This is a new test task',
            'start_date': '2024-07-17 09:00:00',
            'due_date': '2024-07-18 12:00:00',
            'priority': Task.Priority.LOW,
            'category': self.category.pk
        })
        self.assertEqual(response.status_code, 302)  # Check if redirecting to task list upon successful creation
        self.assertTrue(Task.objects.filter(title='New Test Task').exists())

    def test_task_update_view(self):
        """
        Test the task update view to ensure the task is updated successfully.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('update_task', kwargs={'pk': self.task.pk}), {
            'title': 'Updated Test Task',
            'description': 'This is an updated test task',
            'start_date': '2024-07-15 10:00:00',
            'due_date': '2024-07-17 12:00:00',
            'priority': Task.Priority.MEDIUM,
            'category': self.category.pk
        })
        self.assertEqual(response.status_code, 302)  # Check if redirecting to task list upon successful update
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Test Task')

    def test_task_delete_view(self):
        """
        Test the task delete view to ensure the task is deleted successfully.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('task_confirm_delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)  # Check if redirecting to task list upon successful deletion
        self.assertFalse(Task.objects.filter(title='Test Task').exists())

    def test_mark_task_as_completed_view(self):
        """
        Test the view to mark a task as completed and ensure it updates the task status correctly.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('mark_completed', kwargs={'pk': self.task.pk}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_manually_completed)
        self.assertEqual(self.task.status, Task.Status.COMPLETED)

    def test_update_task_status_view(self):
        """
        Test the view to update the task status and ensure it updates the task status correctly.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('update_status', kwargs={'pk': self.task.pk}), {
            'status': Task.Status.IN_PROGRESS
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.IN_PROGRESS)

    def test_task_form_valid(self):
        """
        Test the TaskForm to ensure it is valid with correct data.
        """
        form_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'start_date': '2024-07-15 10:00:00',
            'due_date': '2024-07-16 12:00:00',
            'priority': Task.Priority.HIGH,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid(self):
        """
        Test the TaskForm to ensure it is invalid with incorrect data.
        """
        form_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'start_date': '2024-07-17 12:00:00',
            'due_date': '2024-07-16 10:00:00',  # Due date earlier than start date
            'priority': Task.Priority.HIGH,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_category_form_valid(self):
        """
        Test the CategoryForm to ensure it is valid with correct data.
        """
        form_data = {
            'category_type': Category.CategoryType.PERSONAL,
        }
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid(self):
        """
        Test the CategoryForm to ensure it is invalid with incorrect data.
        """
        form_data = {
            'category_type': Category.CategoryType.OTHER,
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category_name', form.errors)
