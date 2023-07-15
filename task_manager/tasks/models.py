from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from task_manager.statuses.models import Status
from task_manager.users.models import UsersModel


class Task(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), )
    author = models.ForeignKey(UsersModel, on_delete=models.PROTECT,
                               related_name='user_author')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(UsersModel, on_delete=models.PROTECT,
                                 related_name='user_assignee')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
