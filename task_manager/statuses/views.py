from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from task_manager.statuses.models import Status
from task_manager.mixins import LoginRequiredMixin


class StatusesListView(ListView):
    model = Status
    template_name = "statuses/status_list.html"
    context_object_name = "statuses"


class CreateStatus(SuccessMessageMixin, CreateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/create_status.html"
    success_url = reverse_lazy('statuses_list')
    success_message = _("Status created")

    def post(self, request, *args, **kwargs):
    # super().post() maybe raise a ValidationError if it is failure to save
        response = super().post(request, *args, **kwargs)
    # the below code is optional. django has responsed another erorr message
        if not self.object:
            messages.info(request, "Status already exist")
        return response


class UpdateStatus(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = "statuses/update_status.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("Status changed")


class DeleteStatus(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete_status.html"
    success_url = reverse_lazy("statuses_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.warning(request, _("Can't delete status"))
            return redirect(self.get_success_url())
        messages.success(request, _("Status deleted"))
        return super().post(request, *args, **kwargs)
