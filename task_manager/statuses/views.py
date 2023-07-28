from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest

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
        response = super().post(request, *args, **kwargs)
        if not self.object:
            messages.info(request, _("Status already exist"))
        return response


class UpdateStatus(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = "statuses/update_status.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("Status changed")


class DeleteStatus(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/delete_status.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("Status deleted")
    deny_delete_message = _("It is not possible to delete a status because it is in use")
    deny_delete_url = reverse_lazy('labels_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.warning(request, _("Can't delete status"))
            return redirect(self.get_success_url())

        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            return HttpResponseBadRequest(self.deny_delete_message)
