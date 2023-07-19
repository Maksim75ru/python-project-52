from django.test import Client, TestCase
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.users.models import UsersModel
from task_manager.tests import get_test_data


class StatusTestCase(TestCase):
    fixtures = ["task_manager/fixtures/database.json"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = get_test_data()
        self.client = Client()

    def test_status_create(self):
        self.client.post("/statuses/create/",
                         self.test_data["create_status_data"])
        response = self.client.get("/statuses/")
        self.assertContains(response,
                            self.test_data["create_status_result"])
        self.assertContains(response,
                            _("Status created"))

    def test_status_update(self):
        login_user = UsersModel.objects.get(
            username=self.test_data["login_username"],
        )
        self.client.force_login(login_user)
        status = Status.objects.get(name=self.test_data['update_status'])
        self.client.post(f"/statuses/{status.id}/update/",
                         self.test_data["update_status_data"])
        response = self.client.get("/statuses/")
        self.assertContains(response, self.test_data["update_status_result"])
        self.assertContains(response, _("Status changed"))

    def test_status_delete(self):
        login_user = UsersModel.objects.get(
            username=self.test_data["login_username"],
        )
        self.client.force_login(login_user)
        status = Status.objects.get(name=self.test_data['delete_status'])
        self.client.post(f"/statuses/{status.id}/delete/",
                         self.test_data["delete_status_data"])
        response = self.client.get("/statuses/")
        self.assertNotContains(response, self.test_data["delete_status"])
        self.assertContains(response, _("Status deleted"))

    def test_delete_used_status(self):
        login_user = UsersModel.objects.get(
            username=self.test_data["login_username"],
        )
        self.client.force_login(login_user)
        status = Status.objects.get(name=self.test_data['used_status'])
        self.client.post(f"/statuses/{status.id}/delete/",
                         self.test_data["delete_used_status_data"])
        response = self.client.get("/statuses/")
        self.assertNotContains(response, self.test_data["used_status"])
        self.assertContains(response, _("Status deleted"))

    def test_create_already_exist_status(self):
        login_user = UsersModel.objects.get(
            username=self.test_data["login_username"],
        )
        self.client.force_login(login_user)

        existed_status = self.test_data["existed_status_data"]
        response = self.client.post("/statuses/create/", existed_status)
        self.assertContains(response, _("Status already exist"))
