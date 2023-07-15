from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from task_manager.labels.models import Label
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView


class LabelsListView(ListView):
    model = Label
    template_name = "labels/label_list.html"
    context_object_name = "labels"


class CreateLabel(SuccessMessageMixin, CreateView):
    model = Label
    fields = ["name"]
    template_name = "labels/create_label.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("Label created")

    def post(self, request, *args, **kwargs):
    # super().post() maybe raise a ValidationError if it is failure to save
        response = super().post(request, *args, **kwargs)
    # the below code is optional. django has responsed another erorr message
        if not self.object:
            messages.info(request, "Label already exist")
        return response


class UpdateLabel(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    fields = ["name"]
    template_name = "labels/update_label.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("Label changed")


class DeleteLabel(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete_label.html"
    success_url = reverse_lazy("labels_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasklabel_set.exists():
            messages.warning(request, _("Can't delete label"))
            return redirect(self.get_success_url())
        messages.success(request, _("Label deleted"))
        return super().post(request, *args, **kwargs)
