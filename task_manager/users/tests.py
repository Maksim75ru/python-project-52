from django.test import Client, TestCase
from task_manager.users.models import UsersModel
from task_manager.tests import get_test_data
from django.utils.translation import gettext as _


class UserTestCase(TestCase):
    fixtures = ["task_manager/fixtures/database.json"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = get_test_data()
        self.client = Client()

    def test_user_create(self):
        self.client.post("/users/create/",
                         self.test_data["create_user_data"])
        response = self.client.get("/users/")
        self.assertContains(response,
                            self.test_data["create_user_result"])
        self.assertContains(response,
                            _("User is successfully registered"))

    def test_user_update(self):
        login_user = UsersModel.objects.get(
            username=self.test_data["login_username"],
        )
        self.client.force_login(login_user)
        user = UsersModel.objects.get(username=self.test_data["update_user"])
        self.client.post(f"/users/{user.id}/update/",
                         self.test_data["update_user_data"])
        response = self.client.get("/users/")
        self.assertContains(response, self.test_data["update_user_result"])
        self.assertContains(response, _("User is successfully updated"))

    def test_user_delete(self):
        self.client.post("/users/create/",
                         self.test_data["create_user_data"])
        deleted_user = UsersModel.objects.get(
            username=self.test_data["delete_user"],
        )
        self.client.force_login(deleted_user)
        self.client.post(f"/users/{deleted_user.id}/delete/",
                         self.test_data["delete_user_data"])
        response = self.client.get("/users/")
        self.assertNotContains(response, self.test_data["delete_user"])
        self.assertContains(response, _("User is successfully deleted"))

    def test_delete_used_user(self):
        used_user = UsersModel.objects.get(
            username=self.test_data["login_used_username"],
        )
        self.client.force_login(used_user)
        user = UsersModel.objects.get(username=self.test_data["used_user"])
        self.client.post(f"/users/{user.id}/delete/",
                         self.test_data["delete_used_user_data"])
        response = self.client.get("/users/")
        self.assertNotContains(response, self.test_data["used_user"])
        self.assertContains(response, _("User is successfully deleted"))

    def test_create_already_exist_user(self):
        existed_user = self.test_data["existed_user_data"]
        response = self.client.post("/users/create/", existed_user)
        self.assertContains(response, _("User already exist"))
