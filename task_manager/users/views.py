from django.db.models import ProtectedError
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from task_manager.mixins import LoginRequiredMixin, UserRequiredMixin
from task_manager.users.models import UsersModel
from task_manager.users import forms


class ListUsersView(ListView):
    model = UsersModel
    template_name = "users/list_users.html"
    context_object_name = "users_list"


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = forms.UserCreateForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("User is successfully registered")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if not self.object:
            messages.info(request, "User already exist")
        return response


class UserUpdateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserRequiredMixin,
    UpdateView,
):
    model = UsersModel
    form_class = forms.UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users_list")
    success_message = _("User is successfully updated")
    permission_denied_message = _("You have no rights to change another user.")


class UserDeleteView(LoginRequiredMixin, UserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = UsersModel
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_list")
    success_message = _("User is successfully deleted")
    deny_delete_message = _('Unable to delete a user because he is being used')
    deny_delete_url = reverse_lazy('users_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.warning(request, _("Can't delete user"))
            return redirect(self.get_success_url())

        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            return HttpResponseBadRequest(self.deny_delete_message)
