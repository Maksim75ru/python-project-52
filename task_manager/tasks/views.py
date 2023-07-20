from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from task_manager.tasks.models import Task
from task_manager.tasks import filters
from task_manager.tasks import forms
from task_manager.mixins import LoginRequiredMixin
from django.views.generic.list import ListView


class TasksListView(ListView):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = filters.TaskFilter(
            self.request.GET, queryset=self.get_queryset(),
            request=self.request,
        )
        return context


class TaskDetailsView(View):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        task_labels = task.labels.values_list("name", flat=True)
        return render(
            request,
            "tasks/task_details.html",
            context={
                "task": task, "task_labels": task_labels
            },
        )


class CreateTask(SuccessMessageMixin, CreateView):
    form_class = forms.TaskCreateForm
    template_name = "tasks/create_task.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task successfully created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if not self.object:
            messages.info(request, "Task already exist")
        return response


class UpdateTask(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = forms.TaskUpdateForm
    template_name = "tasks/update_task.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task successfully changed")


class DeleteTask(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/delete_task.html"
    success_url = reverse_lazy("tasks_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.warning(request, _("Can't delete task"))
            return redirect(self.get_success_url())
        messages.success(request, _("Task successfully deleted"))
        return super().post(request, *args, **kwargs)
