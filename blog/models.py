from django.db import models
from secrets import token_hex
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class PostManager(models.Manager):
    """
    Filter approved, pended and declined posts
    """
    def filter_approved(self):
        return self.filter(status=Post.APPROVED)

    def filter_pending(self):
        return self.filter(status=Post.PENDING)

    def filter_declined(self):
        return self.filter(status=Post.DECLINED)


class Post(models.Model):
    """
    Posts in blog
    """

    APPROVED = "approved"
    DECLINED = "declined"
    PENDING = "pending"

    # Post status
    STATUS = (
        (PENDING, _("Pending")),   # Default
        (APPROVED, _("Approved")),
        (DECLINED, _("Declined"))
    )

    title = models.CharField(_("Title"), max_length=250, blank=False, null=False)
    content = RichTextField(_("Context"), blank=False, null=False)
    date_posted = models.DateField(_("Date posted"), default=timezone.now)
    status = models.CharField(_("Status"), max_length=10, choices=STATUS, default=PENDING)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Author"))
    slug = models.SlugField(unique=True, blank=False, null=True, default="")

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Url for post (PostDetailView)
        """
        return reverse("blog:post-detail", kwargs={"slug": self.slug})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Save post
        """
        if not self.slug:
            self.slug = slugify(self.title + "-" + token_hex(5), allow_unicode=True)
        super(Post, self).save(force_update, using, update_fields)


class Comment(models.Model):
    content = RichTextField(_("Context"), blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Author"))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("Post"))
    date_posted = models.DateField(_("Date posted"), default=timezone.now)

    def __str__(self):
        return f"{self.author.username}, {self.post.title}"

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
