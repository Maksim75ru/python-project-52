from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse


def error(request):
    foo()
    return HttpResponse('You shouldn\'t be seeing this')


class HomePageView(TemplateView):
    template_name = "base.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    form_class = AuthenticationForm
    next_page = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "You are logged in")
        return super().form_valid(form)

    def form_invalid(self, form):
        error_login_message = "Please enter correct username and password."
        messages.error(self.request, error_login_message)
        return super().form_invalid(form)


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy("home")
    success_message = "You are logged out"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
