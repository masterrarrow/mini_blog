from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from secrets import token_hex
from PIL import Image
import os


class UserGroup(models.Model):
    """
    User groups (Defaults for user)
    """
    name = models.CharField(_("Name"), max_length=20, blank=False, null=False)
    pre_moderation = models.BooleanField(_("Pre moderation"), default=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('User Group')
        verbose_name_plural = _('User Groups')


def upload_image(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]

        # Generate an encoded name for a picture
        filename = '{}.{}'.format(token_hex(8), ext)

        return os.path.join(path, filename)

    return wrapper


class Profile(models.Model):
    """
    User profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    birth_date = models.DateField(_("Birth date"), null=True, blank=True)
    email_confirmed = models.BooleanField(_("Email confirmed"), default=False)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, verbose_name=_("User group"))
    image = models.ImageField(default="default_user.jpg",
                              upload_to=upload_image("profile_pics"),
                              verbose_name=_("Profile Picture"))

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def save(self):
        """
        User image
        """
        super().save()

        img = Image.open(self.image.path)

        if img.height > 150 and img.width > 150:
            # Scale the image
            output_size = (150, 150)
            img.thumbnail(output_size)

            img.save(self.image.path)
