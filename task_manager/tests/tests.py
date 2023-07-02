import logging

from django.test import Client, SimpleTestCase, TestCase, RequestFactory, TransactionTestCase

from task_manager.users.models import UsersModel
from task_manager.views import HomePageView


c = Client()


class SimpleTest(TestCase):
    databases = 'postgresql'

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = UsersModel.objects.update_or_create(
            username='petya',
            defaults={
                "password": "petrov1111"
            },
        )

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        request.user = self.user

        response = HomePageView.as_view()(request)
        self.assertEqual(response.status_code, 200)
