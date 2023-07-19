import django_filters
from django import forms
from task_manager.tasks.models import Status, UsersModel, Label, Task
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request", None)
        super().__init__(*args, **kwargs)

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        to_field_name="name",
        label=_("Status"),
        label_suffix="",
    )
    author = django_filters.ModelChoiceFilter(
        queryset=UsersModel.objects.all(),
        to_field_name="username",
        label=_("Author"),
        label_suffix="",
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=UsersModel.objects.all(),
        to_field_name="username",
        label=_("Executor"),
        label_suffix="",
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        to_field_name="name",
        label=_("Label"),
        label_suffix="",
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_by_authorized",
        widget=forms.CheckboxInput(),
        label=_("Only my tasks"),
        label_suffix="",
    )

    class Meta:
        model = Task
        fields = ["status", "author", "executor", "labels", "self_tasks"]

    def filter_by_authorized(self, queryset, author, value):
        authorized_user = getattr(self.request, "user", None)

        if value:
            return queryset.filter(author=authorized_user.id)
        else:
            return queryset
