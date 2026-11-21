from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
import datetime

class TaskManagerTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user_a = User.objects.create_user(username='user_a', password='password123')
        self.user_b = User.objects.create_user(username='user_b', password='password123')

        # Create tasks for user A
        self.task_a1 = Task.objects.create(
            owner=self.user_a,
            title='User A Task 1',
            description='Description for task 1',
            due_date=datetime.date.today(),
            completed=False
        )
        self.task_a2 = Task.objects.create(
            owner=self.user_a,
            title='User A Task 2',
            completed=True
        )

        # Create task for user B
        self.task_b1 = Task.objects.create(
            owner=self.user_b,
            title='User B Task 1',
            completed=False
        )

        self.client = Client()

    def test_signup(self):
        """Test user signup and auto-login."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, 'newuser')

    def test_unauthenticated_redirect(self):
        """Test unauthenticated user is redirected to login page."""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_task_list_isolation(self):
        """Test that user only sees their own tasks."""
        self.client.login(username='user_a', password='password123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertIn(self.task_a1, tasks)
        self.assertIn(self.task_a2, tasks)
        self.assertNotIn(self.task_b1, tasks)

    def test_task_create(self):
        """Test creating a new task sets owner=request.user."""
        self.client.login(username='user_a', password='password123')
        response = self.client.post(reverse('task_create'), {
            'title': 'New Created Task',
            'description': 'Created via view',
            'due_date': '2026-12-31'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        new_task = Task.objects.get(title='New Created Task')
        self.assertEqual(new_task.owner, self.user_a)

    def test_task_update(self):
        """Test editing a task owned by user."""
        self.client.login(username='user_a', password='password123')
        response = self.client.post(reverse('task_update', kwargs={'pk': self.task_a1.pk}), {
            'title': 'Updated Title',
            'description': self.task_a1.description,
            'completed': True
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.task_a1.refresh_from_db()
        self.assertEqual(self.task_a1.title, 'Updated Title')
        self.assertTrue(self.task_a1.completed)

    def test_task_toggle_complete(self):
        """Test toggling task completion status."""
        self.client.login(username='user_a', password='password123')
        self.assertFalse(self.task_a1.completed)
        response = self.client.post(reverse('task_toggle_complete', kwargs={'pk': self.task_a1.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.task_a1.refresh_from_db()
        self.assertTrue(self.task_a1.completed)

    def test_task_delete(self):
        """Test deleting a task."""
        self.client.login(username='user_a', password='password123')
        response = self.client.post(reverse('task_delete', kwargs={'pk': self.task_a1.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=self.task_a1.pk).exists())

    def test_cross_user_security_returns_404(self):
        """
        CRITICAL SECURITY REQUIREMENT:
        Test that user B attempting to edit, delete, or toggle user A's task gets HTTP 404.
        """
        self.client.login(username='user_b', password='password123')

        # Edit user A's task
        response_edit = self.client.get(reverse('task_update', kwargs={'pk': self.task_a1.pk}))
        self.assertEqual(response_edit.status_code, 404)

        # Delete user A's task
        response_delete = self.client.get(reverse('task_delete', kwargs={'pk': self.task_a1.pk}))
        self.assertEqual(response_delete.status_code, 404)

        # Toggle user A's task
        response_toggle = self.client.post(reverse('task_toggle_complete', kwargs={'pk': self.task_a1.pk}))
        self.assertEqual(response_toggle.status_code, 404)
