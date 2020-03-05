from pathlib import Path
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.encoding import force_bytes
from django.contrib.auth import login, authenticate
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.tokens import account_activation_token
from users.tasks import send_email
from blog.models import Post
import logging


def activate(request, uidb64, token):
    """
    Activate account (confirm email)
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        profile = user.profile
        profile.email_confirmed = True
        profile.save()
        user.save()
        messages.success(request, _("Your email has been confirmed. Now you can sign in"))
    else:
        messages.error(request, _("Wrong activation data. Your account has not been activated"))

    return redirect("user:sign-in")


class SignUpView(View):
    """
    Register
    """

    form_class = UserRegisterForm
    template_name = "users/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")

        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")

        form = self.form_class(request.POST)
        if form.is_valid():
            if User.objects.filter(email=request.POST["email"].lower()).first():
                messages.warning(request, _("User with this credential already exists"))
                return redirect("user:sign-up")

            user = form.save()
            user.refresh_from_db()
            # Email is case-insensitive
            user.email = user.email.lower()
            # Email isn't confirmed
            user.is_active = False
            # Profile created in signals
            user.profile.birth_date = form.cleaned_data.get("birth_date")
            user.save()

            content = render_to_string("users/activation_email.html", {
                "user": user.first_name,
                "domain": get_current_site(request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })

            # Send a confirmation email
            send_email.delay(subject=str(_("Please Activate Your Account")), email=user.email, content=content)

            messages.success(request, _("Instructions for activating your account has been emailed to you"))
            return redirect("home")

        return redirect("user:sign-up")


class LoginView(View):
    """
    Login
    """

    form_class = UserLoginForm
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")

        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(email=email.lower()).first()

            if user and user.profile.email_confirmed:
                usr = authenticate(username=user.username, password=password)
                try:
                    login(request, usr)
                except:
                    messages.warning(request, _("Wrong user credentials or your email has not been confirmed"))
                    return redirect("user:sign-in")
            else:
                messages.warning(request, _("Wrong user credentials or your email has not been confirmed"))
                return redirect("user:sign-in")

        messages.success(request, _(f"Successfully signed in as ") + request.user.username)

        if request.GET.get("next"):
            return redirect(request.GET.get("next"))

        return redirect("home")


class UserProfileView(LoginRequiredMixin, View):
    """
    Update profile
    """

    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)

        # Number of approved user posts
        approved = Post.objects.filter(author=user).filter(status=Post.APPROVED).count()
        # Posts under review
        pending = Post.objects.filter(author=user).filter(status=Post.PENDING).count()
        # Posts declined to publication
        declined = Post.objects.filter(author=user).filter(status=Post.DECLINED).count()

        context = {
            "user": user,
            "user_form": user_form,
            "profile_form": profile_form,
            "approved": approved,
            "pending": pending,
            "declined": declined,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            if request.FILES:
                user = User.objects.filter(username=request.user.username).first()
                if user.profile.image != "default_user.jpg":
                    __, user_image = str(user.profile.image).split("/")
                    # Delete an old profile image
                    try:
                        Path(settings.MEDIA_ROOT).joinpath(str(user.profile.image)).unlink()
                    except:
                        logging.warning(f"Cannot delete user image {str(user.profile.image)}")

            profile_form.save()

            messages.success(request, _("You account has been updated"))

        return redirect("user:profile")


class UserDeleteView(LoginRequiredMixin, View):
    """
    Delete user
    """

    template_name = "users/user_confirm_delete.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("user:sign-in")

        # Check user
        user = get_object_or_404(User, id=self.kwargs.get("pk"))
        if request.user == user:
            return render(request, self.template_name)

        return redirect("home")

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.kwargs.get("pk"))
        if request.user == user:
            logout(request)
            # User profile image deleted in signals
            user.delete()
        else:
            messages.error(request, _("You don't have the right permissions to do that"))

        return redirect("home")


class PasswordResetRequestView(View):
    """
    Request a user password reset
    """

    template_name = "users/request_password_reset.html"

    def get(self, requset, *args, **kwargs):
        return render(requset, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, _("User with this email does not exist"))
            return redirect("user:sign-up")

        content = render_to_string("users/password_reset_email.html", {
            "user": user.first_name,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": PasswordResetTokenGenerator().make_token(user=user),
        })

        # Send a confirmation email
        send_email.delay(subject=str(_("Password reset confirmation")), email=user.email, content=content)

        messages.success(request, _("Instructions to reset your password has been emailed to you"))
        return redirect("home")
