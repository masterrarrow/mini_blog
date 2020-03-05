import logging
from PIL import Image
from io import BytesIO
from pathlib import Path
from requests import get
from secrets import token_hex
from django.conf import settings
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import redirect
from users.models import Profile, UserGroup


@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    """
    When user logged in with social account store his profile image and set email_confirmed=True
    """
    if sociallogin.account.provider == "google":
        user_data = user.socialaccount_set.filter(provider="google")[0].extra_data
        image_url = user_data["picture"]

        response = get(image_url, stream=True)
        file = BytesIO(response.content)
        del response

        img = Image.open(file)
        # Create a thumbnail
        img.thumbnail((150, 150))

        # Generate an encoded name for a picture
        filename = '{}.{}'.format(token_hex(8), "jpg")
        directory = Path.cwd().parent.joinpath(settings.MEDIA_ROOT).joinpath('profile_pics/')
        image_path = directory.joinpath(filename)

        try:
            img.save(image_path)
            user.profile.image = f"profile_pics/{filename}"
        except Exception as e:
            # Delete file if an error occurs (default image was set as a profile image)
            Path(image_path).unlink()
            logging.warning(f"Cannot save user profile image {str(filename)}")

        user.profile.email_confirmed = True
        user.profile.save()

        return redirect("home")


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a user profile when registering a new user
    """
    if created:
        profile = Profile()
        profile.user = instance
        # Default group users without permissions
        user_group = UserGroup.objects.filter(pre_moderation=True).first()
        profile.user_group = user_group
        profile.save()


@receiver(pre_delete, sender=User)
def delete_profile_image(sender, instance, **kwargs):
    """
    Delete user profile image
    """
    if instance.profile.image != "default_user.jpg":
        try:
            Path(settings.MEDIA_ROOT).joinpath(str(instance.profile.image)).unlink()
        except:
            logging.warning(f"Cannot delete user image {str(instance.profile.image)}")
