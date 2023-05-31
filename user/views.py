from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from user.forms import UserRegisterForm, EditProfileForm
from user.models import Profile


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("user:login")

    success_message = (
        "Your account is created successfully, please, "
        "login with your email and password"
    )


class UserEditView(SuccessMessageMixin, UpdateView):
    form_class = EditProfileForm
    template_name = "user/edit_user_data.html"
    success_url = reverse_lazy("movie:movie-list")

    success_message = "Your settings has been successfully updated."

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileCreateView(SuccessMessageMixin, CreateView):
    model = Profile
    template_name = "user/create_user_profile_page.html"
    fields = ("bio", "image",)

    success_message = "Your profile has been successfully created."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy("movie:movie-list")


class ProfileEditView(SuccessMessageMixin, UpdateView):
    model = Profile
    template_name = "user/edit_profile_page.html"
    fields = ("bio", "image")
    success_url = reverse_lazy("movie:movie-list")

    success_message = "Your profile has been successfully updated."


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "user/password_change_form.html"
    success_url = reverse_lazy("user:password-success")


def password_success_view(request):
    return render(request, "user/password_change_done.html", {})
