from django.contrib.auth.models import AbstractUser


class UsersModel(AbstractUser):

    def __str__(self):
        return self.get_full_name()