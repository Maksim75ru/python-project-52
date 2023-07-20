from django.test import Client, TestCase
from task_manager.tasks.models import Task
from task_manager.users.models import UsersModel
from task_manager.tests import get_test_data
from django.urls import reverse
from django.utils.translation import gettext as _


class TaskTestCase(TestCase):
    fixtures = ["task_manager/fixtures/database.json"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = get_test_data()
        self.client = Client()

    def test_task_create(self):
        login_user = UsersModel.objects.get(
            username=self.test_data["login_username"],
        )
        self.client.force_login(login_user)
        self.client.post(reverse("task_create"),
                         self.test_data["create_task_data"])
        response = self.client.get("/tasks/")
        self.assertContains(response,
                            self.test_data["create_task_result"])
        self.assertContains(response,
                            _("Task successfully created"))

    def test_task_update(self):
        login_user = UsersModel.objects.get(
            username=self.test_data["login_username"],
        )
        self.client.force_login(login_user)
        task = Task.objects.get(name=self.test_data["update_task"])
        self.client.post(f"/tasks/{task.id}/update/",
                         self.test_data["update_task_data"])
        response = self.client.get("/tasks/")
        self.assertContains(response, self.test_data["update_task_result"])
        self.assertContains(response, _("Task successfully changed"))

    def test_task_delete(self):
        login_user = UsersModel.objects.get(
            username=self.test_data["login_username"],
        )
        self.client.force_login(login_user)
        task = Task.objects.get(name=self.test_data["delete_task"])
        self.client.post(f"/tasks/{task.id}/delete/",
                         self.test_data["delete_task_data"])
        response = self.client.get("/tasks/")
        self.assertNotContains(response, self.test_data["delete_task"])
        self.assertContains(response, _("Task successfully deleted"))

    def test_create_already_exist_task(self):
        login_user = UsersModel.objects.get(
            username=self.test_data["login_username"],
        )
        self.client.force_login(login_user)
        response = self.client.post("/tasks/create/",
                                    self.test_data["existed_task_data"])
        self.assertContains(response, _("Task already exist"))
