from django.test import TestCase
from blog.models import Post, Comment
from users.tests import create_test_user


def create_test_post():
    post = Post()
    post.title = "New post"
    post.date_posted = "2020-02-08"

    user = create_test_user()
    post.author = user
    post.save()

    return post, user


class TestModels(TestCase):
    def test_post_model(self):
        post = create_test_post()

        post_record = Post.objects.get(pk=1)
        self.assertEqual(post_record, post[0], "Test Post model")

    def test_comment_model(self):
        post = create_test_post()

        comment = Comment()
        comment.author = post[1]
        comment.post = post[0]
        comment.content = "Content"
        comment.date_posted = "2020-02-08"
        comment.save()

        comment_record = Comment.objects.get(pk=1)
        self.assertEqual(comment_record, comment, "Test Comment model")
