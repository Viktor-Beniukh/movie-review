from django.urls import path
from django.contrib.auth import views as auth_views

from user.views import (
    UserRegisterView,
    UserEditView,
    UserProfileCreateView,
    ProfileEditView,
    password_success_view,
)


app_name = "user"


urlpatterns = [
    path(
        "register/",
        UserRegisterView.as_view(),
        name="register"
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="registration/logout.html"
        ),
        name="logout",
    ),
    path(
        "edit-user-data/",
        UserEditView.as_view(),
        name="edit-user-data"
    ),
    path(
        "<int:pk>/edit-profile/",
        ProfileEditView.as_view(),
        name="edit-profile"
    ),
    path(
        "profile-create/",
        UserProfileCreateView.as_view(),
        name="profile-create"
    ),
    path(
        "password-success/",
        password_success_view,
        name="password-success"
    ),
]
