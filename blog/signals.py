from django.utils import timezone
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from blog.models import Post, Comment
from users.tasks import send_email


@receiver(pre_save, sender=Post)
def post_status_changed(sender, instance, **kwargs):
    """
    Notify user when the status of his post changed
    """
    if instance.pk:
        saved_post = Post.objects.get(pk=instance.pk)
        # Set current date as publication date
        instance.date_posted = timezone.now()

        if instance.status != saved_post.status:
            site = Site.objects.get_current()
            content = render_to_string("blog/post_status_notification_email.html", {
                "name": instance.author.first_name,
                "post": instance,
                "link": f"{site.domain}/post/{instance.slug}/",
                "domain": site.domain,
            })
            user = instance.author

            # Send a notification email
            send_email.delay(subject=str(_("Your post has been ")) + f"{instance.status}" +
                             str(_(" to publication")), email=user.email, content=content)


@receiver(pre_save, sender=Post)
def post_status(sender, instance, **kwargs):
    """
    Set post status
    """
    try:
        # Check if user post moderation is needed
        if not instance.author.profile.user_group.pre_moderation:
            instance.status = Post.APPROVED
    except:
        instance.status = Post.PENDING


@receiver(pre_save, sender=Comment)
def notify_about_comment(sender, instance, **kwargs):
    """
    Notify user about a new comment on his post
    """

    comment = Comment.objects.filter(pk=instance.pk)
    if comment:
        # Do not notify user if someone edited an existing comment
        return

    # Do not notify user about his comment on his own post
    if instance.author != instance.post.author:
        site = Site.objects.get_current()
        content = render_to_string("blog/comment_notification_email.html", {
            "name": instance.post.author.first_name,
            "comment_author": instance.author.username,
            "post": instance.post,
            "link": f"{site.domain}/post/{instance.post.slug}/",
            "domain": site.domain,
        })
        user = instance.post.author

        # Send a notification email
        send_email.delay(subject=str(_("New Comment on your post")), email=user.email, content=content)
