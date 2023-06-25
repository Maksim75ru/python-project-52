from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _


class HomePageView(TemplateView):
    template_name = "base.html"


class UserLoginView(SuccessMessageMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        success_message = _('You logged in')
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

        return render(request, "login.html", {"form": form})


# class UserLogoutView(TemplateView):
#     pass
