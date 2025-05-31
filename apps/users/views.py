from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from apps.users.models import User
from apps.users.forms import UserForm
from apps.users.decorators import role_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth import logout
from django.shortcuts import redirect

superadmin_only = role_required("SUPERADMIN")


@method_decorator(superadmin_only, name="dispatch")
class UserList(generic.ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


@method_decorator(superadmin_only, name="dispatch")
class UserCreate(generic.CreateView):
    model = User
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")


@method_decorator(superadmin_only, name="dispatch")
class UserUpdate(generic.UpdateView):
    model = User
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")


@method_decorator(superadmin_only, name="dispatch")
class UserDelete(generic.DeleteView):
    model = User
    template_name = "partials/confirm_delete.html"
    success_url = reverse_lazy("user_list")


@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})


def logout_view(request):
    logout(request)
    return redirect("login")
