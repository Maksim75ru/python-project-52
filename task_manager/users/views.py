from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from task_manager.users.models import UsersModel
from task_manager.users.forms import UserForm


class ListUsersView(TemplateView):

    def get(self, request, *args, **kwargs):
        users_list = UsersModel.objects.all()
        return render(request, "users/list_users.html", {"users_list": users_list})


class UserCreateView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, "users/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/users")

        return render(request, "users/create.html", {"form": form})


class UserUpdateView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = UsersModel.objects.get(id=user_id)
        form = UserForm(instance=user)
        return render(request, "users/update.html", {"form": form, "user_id": user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = UsersModel.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("/users")

        return render(request, "users/update.html", {"form": form, "user_id": user_id})
