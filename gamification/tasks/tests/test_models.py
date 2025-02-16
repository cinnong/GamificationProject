from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import UserProfile, Task, CustomTask, UserTaskCompletion, UserCustomTaskCompletion


class UserProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = self.user.userprofile

    def test_calculate_exp_to_level(self):
        self.assertEqual(self.profile.calculate_exp_to_level(), 100)
        self.profile.level = 3
        self.assertEqual(self.profile.calculate_exp_to_level(), 200)

    def test_add_exp_levels_up_correctly(self):
        self.profile.add_exp(200)  # Exceeds level-up requirement
        self.assertEqual(self.profile.level, 2)
        self.assertLess(self.profile.exp, self.profile.calculate_exp_to_level())


class TaskModelTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            difficulty="easy",
            exp_reward=50,
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.difficulty, "easy")
        self.assertFalse(self.task.is_completed)

    def test_reset_task(self):
        self.task.is_completed = True
        self.task.reset_task()
        self.assertFalse(self.task.is_completed)
        self.assertIsNotNone(self.task.last_reset)


class CustomTaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = self.user.userprofile
        self.custom_task = CustomTask.objects.create(
            title="Custom Task",
            description="Test Custom Task",
            exp_reward=50,
            user=self.profile,
        )

    def test_schedule_deletion_sets_delete_at(self):
        self.custom_task.schedule_deletion()
        self.assertIsNotNone(self.custom_task.delete_at)

    def test_custom_task_creation(self):
        self.assertEqual(self.custom_task.title, "Custom Task")
        self.assertEqual(self.custom_task.exp_reward, 50)
        self.assertFalse(self.custom_task.is_completed)


class UserTaskCompletionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = self.user.userprofile
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            difficulty="easy",
            exp_reward=50,
        )

    def test_task_completion_creation(self):
        completion = UserTaskCompletion.objects.create(user=self.profile, task=self.task)
        self.assertIsNotNone(completion.completed_at)
