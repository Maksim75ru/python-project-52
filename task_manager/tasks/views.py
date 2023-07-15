from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from task_manager.tasks import forms
from task_manager.mixins import LoginRequiredMixin


class TasksListView(ListView):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"


class TaskDetailsView(View):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        return render(
            request,
            "tasks/task_details.html",
            context={
                "task": task
            },
        )

class CreateTask(SuccessMessageMixin, CreateView):
    form_class = forms.TaskCreateForm
    template_name = "tasks/create_task.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
    # super().post() maybe raise a ValidationError if it is failure to save
        response = super().post(request, *args, **kwargs)
    # the below code is optional. django has responsed another erorr message
        if not self.object:
            messages.info(request, "Task already exist")
        return response


class UpdateTask(SuccessMessageMixin, LoginRequiredMixin,UpdateView):
    model = Task
    form_class = forms.TaskUpdateForm
    template_name = "tasks/update_task.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task changed")


class DeleteTask(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/delete_task.html"
    success_url = reverse_lazy("tasks_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.warning(request, _("Can't delete task"))
            return redirect(self.get_success_url())
        messages.success(request, _("Task deleted"))
        return super().post(request, *args, **kwargs)
