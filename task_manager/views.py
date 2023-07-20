from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache


class HomePageView(TemplateView):
    template_name = "base.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    form_class = AuthenticationForm
    next_page = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)

    def form_invalid(self, form):
        error_login_message = _("Please enter correct username and password.")
        messages.error(self.request, error_login_message)
        return super().form_invalid(form)


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy("home")
    success_message = _("You are logged out")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
