from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.users.models import UsersModel
from task_manager.users.forms import UserForm
from django.contrib.messages.views import SuccessMessageMixin


class ListUsersView(ListView):
    model = UsersModel
    template_name = "users/list_users.html"
    context_object_name = "users_list"


class UserCreateView(SuccessMessageMixin, CreateView):

    model = UsersModel
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created")
            return redirect("login")

        messages.warning(request, "Can't create user")
        return render(request, "users/create.html", {"form": form})


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = UsersModel
    form_class = UserForm
    template_name = "users/update.html"
    success_url = reverse_lazy('users_list')
    success_message = "User changed"
    permission_denied_message = "Can't edit user"


class UserDeleteView(DeleteView):

    model = UsersModel
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_id = self.object.pk
        if UsersModel.objects.filter(pk=user_id).exists():
            messages.success(request, "User deleted")
            return super().post(request, *args, **kwargs)
        messages.warning(request, "Can't delete used user")
        return redirect(self.get_success_url)
