from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from task_manager.users.models import UsersModel
from task_manager.users.forms import UserForm


class ListUsersView(TemplateView):

    def get(self, request, *args, **kwargs):
        users_list = UsersModel.objects.all()
        return render(request, "users/list_users.html", {"users_list": users_list})


class UserFormCreateView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, "users/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/users")

        return render(request, "users/create.html", {"form": form})
