from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile, UserGroup
from users.forms import UserLoginForm, UserRegisterForm
from users.tasks import send_email


def create_test_user():
    user = User()
    user.username = "user"
    user.set_password("password")
    user.email = "user_email@gmail.com"
    user.save()

    return user


def create_test_group():
    group = UserGroup()
    group.name = "test"
    group.save()

    return group


class TestUserModels(TestCase):
    def test_user_group_model(self):
        group = create_test_group()

        group_record = UserGroup.objects.get(pk=1)
        self.assertEqual(group_record, group, "Test UserGroup model")

    def test_profile_model(self):
        group = create_test_group()
        user = create_test_user()

        profile = Profile()
        profile.birth_date = "2020-02-08"
        profile.email_confirmed = False
        profile.user = user
        profile.user_group = group
        profile.save()

        profile_record = Profile.objects.get(pk=1)
        self.assertEqual(profile_record, profile, "Test Profile model")


class TestUserForms(TestCase):
    def test_login_form(self):
        login = UserLoginForm()
        login.email = "email"
        login.password = "password"

        self.assertEqual(login.is_valid(), False, "Test UserLoginForm")

    def test_register_form(self):
        register = UserRegisterForm()
        register.email = "email@email.com"
        register.password1 = "password"
        register.password2 = "password2"

        self.assertEqual(register.is_valid(), False, "Test UserRegisterForm")


class TestSendEmail(TestCase):
    def test_send_email(self):
        user = create_test_user()
        content = "Test Email"

        try:
            send_email(subject="Test Email", user=user, content=content)
            result = True
        except:
            result = False

        self.assertEqual(result, True, "Test send_email")
