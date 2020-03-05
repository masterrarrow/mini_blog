from django import forms
from blog.models import Post, Comment


class PostStatusForm(forms.ModelForm):
    """
    Form for changing a post status (for admin users)
    """

    class Meta:
        """
        Configure form
        """

        model = Post
        fields = ["status"]


class CommentForm(forms.ModelForm):
    """
    Comment form
    """
    id = forms.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = ["id", "content"]
