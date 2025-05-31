# apps/users/urls.py
from django.urls import path
from .views import UserList, UserCreate, UserUpdate, UserDelete, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", UserList.as_view(), name="user_list"),            # /users/
    path("new/", UserCreate.as_view(), name="user_create"),     # /users/new/
    path("<int:pk>/edit/", UserUpdate.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDelete.as_view(), name="user_delete"),
    path("profile/", profile_view, name="user_profile"),
    path("logout/", LogoutView.as_view(template_name="logout_success.html"), name="logout"),
]