from task_manager.users.models import UsersModel
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    class Meta:
        model = UsersModel
        fields = ("username", "first_name", "last_name")


class UserUpdateForm(UserCreateForm):
    pass
