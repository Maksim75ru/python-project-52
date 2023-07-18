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
    success_message = _("User created")

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
    success_message = _("User changed")
    permission_denied_message = _("Can't edit user")


class UserDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    model = UsersModel
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.warning(request, _("Can't delete user"))
            return redirect(self.get_success_url())
        messages.success(request, _("User deleted"))
        return super().post(request, *args, **kwargs)
