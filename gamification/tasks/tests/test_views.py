from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task, CustomTask, UserProfile, UserTaskCompletion, UserCustomTaskCompletion

class SignalTests(TestCase):
    def test_create_user_profile_signal(self):
        # Create a new user
        user = User.objects.create_user(username='testuser', password='password')
        
        # Check if the UserProfile instance is created
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        
class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.create_custom_task_url = reverse('create_custom_task')
        self.profile_view_url = reverse('profile')
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_register_view(self):
        response = self.client.post(self.register_url, {'username': 'testuser2', 'email': 'test@email.com', 'password1': 'lol123lol', 'password2': 'lol123lol'})
        self.assertEqual(response.status_code, 302, msg=f"Response content: {response.content}")
        self.assertTrue(User.objects.filter(username='testuser2').exists())

    def test_login_view(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'password'})
        self.assertRedirects(response, reverse('index'))
        
    def test_logout_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        
    def test_create_custom_task_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.create_custom_task_url, {'title': 'Custom Task', 'description': 'Test Custom Task', 'exp_reward': 50})
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(CustomTask.objects.filter(title='Custom Task').exists())

    def test_profile_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.profile_view_url)
        self.assertEqual(response.status_code, 200)

class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            difficulty="easy",
            exp_reward=50,
        )
        self.client.login(username='testuser', password='password')

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_list.html')

    def test_task_list_filtering(self):
        response = self.client.get(reverse('task_list') + '?difficulty=easy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task, response.context['tasks'])

    def test_complete_task(self):
        response = self.client.post(reverse('complete_task', args=[self.task.id]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(UserTaskCompletion.objects.filter(user=self.user.userprofile, task=self.task).exists())


class CustomTaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = self.user.userprofile
        self.custom_task = CustomTask.objects.create(
            title="Custom Task",
            description="Test Custom Task",
            exp_reward=50,
            user=self.profile,
            is_validated=True,
        )
        self.client.login(username='testuser', password='password')

    def test_complete_custom_task(self):
        response = self.client.post(reverse('complete_custom_task', args=[self.custom_task.id]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(UserCustomTaskCompletion.objects.filter(user=self.profile, task=self.custom_task).exists())

    def test_custom_task_list(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.custom_task, response.context['custom_tasks'])

    def test_invalid_custom_task(self):
        self.custom_task.is_validated = False
        self.custom_task.save()
        response = self.client.post(reverse('complete_custom_task', args=[self.custom_task.id]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertFalse(UserCustomTaskCompletion.objects.filter(user=self.profile, task=self.custom_task).exists())
