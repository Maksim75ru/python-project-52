from django.urls import reverse_lazy
from django.test import (
    SimpleTestCase,
    TestCase,
    override_settings,
    Client,
    TransactionTestCase

)
from task_manager.users.models import UsersModel


TEST_USER = {
    "first_name": "Admin",
    "last_name": "Adminov",
    "username": "admin777",
    "password1": "odmen1111",
    "password2": "odmen1111",
    "password": "odmen1111",
}


class SimpleTest(SimpleTestCase):

    def test_open_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class UserTestCreate(TestCase):

    def test_create_user(self):
        response = self.client.get(reverse_lazy("users_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_redirect_user(self):
        response = self.client.post(
            reverse_lazy("users_create"),
            TEST_USER,
        )
        self.assertRedirects(response, reverse_lazy("login"))
        user = UsersModel.objects.get(pk=1)
        self.assertEqual(user.username, TEST_USER.get("username"))


class UserTestUpdate(TransactionTestCase):

    def setUp(self) -> None:
        UsersModel.objects.create_user(
            first_name="Steven",
            last_name="King",
            username="steveking",
        )

    def test_redirect_after_update(self):
        user = UsersModel.objects.all().first()

        self.client.force_login(user=user)
        response = self.client.post(
            reverse_lazy(
                "users_update",
                kwargs={"pk": user.id}
            ),
            **TEST_USER
        )

        self.assertRedirects(response, reverse_lazy("users_list"))
        self.assertEqual(user.last_name, TEST_USER.get('last_name'))
