from django.test import TestCase
from django.contrib.auth import get_user_model

class UserManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="testuser@exam.com",
            password="testpass123",
        )
        self.assertEqual(user.username,"testuser")
        self.assertEqual(user.email, "testuser@exam.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="testsuperuser",
            email="testsuperuser@exam.com",
            password="testpass123",
        )
        self.assertEqual(user.username,"testsuperuser")
        self.assertEqual(user.email, "testsuperuser@exam.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


