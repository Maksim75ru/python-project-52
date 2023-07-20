from django import forms
from django.utils.translation import gettext as _
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import UsersModel


class TaskCreateForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=UsersModel.objects.all(),
        label=_("Executor"),
        widget=forms.Select(attrs={"label": "executor"}),
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_("Status"),
        widget=forms.Select(attrs={"label": "status"}),
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        label=_("Labels"),
        widget=forms.SelectMultiple(attrs={"label": "labels"}),
        required=False,
    )

    class Meta:
        model = Task
        fields = ["name", "description", "executor", "status", "labels"]
        widgets = {
            "name": forms.TextInput(attrs={"label": "name"}),
            "description": forms.TextInput(attrs={"label": "description"}),
            "executor": forms.TextInput(attrs={"label": "executor"}),
            "status": forms.TextInput(attrs={"label": "status"}),
            "labels": forms.TextInput(attrs={"label": "labels"}),
        }


class TaskUpdateForm(TaskCreateForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
