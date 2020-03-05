from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, CreateView,
    UpdateView, DeleteView)
from django.db.models import Q
from blog.models import Post, Comment
from blog.forms import PostStatusForm, CommentForm


class PostListView(ListView):
    """
    Show all posts or posts by a user approved to publication (status='approved').
    Show posts under review - (status='pending') and declined to publication (status='declined').
    Additional filters: search str and post date.
    """

    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        # Basic: Post status
        status = self.request.GET.get("status")
        if status == "pending":
            # Show posts under review
            result = self.model.objects.filter_pending().order_by("-date_posted")\
                .prefetch_related("author").prefetch_related("author__profile")
        elif status == "declined":
            # Show posts declined to publication
            result = self.model.objects.filter_declined().order_by("-date_posted")\
                .prefetch_related("author").prefetch_related("author__profile")
        elif self.request.user.is_staff:
            # Show all posts (for admin users)
            result = self.model.objects.all().order_by("-date_posted")\
                .prefetch_related("author").prefetch_related("author__profile")
        else:
            # Show only approved posts (default)
            result = self.model.objects.filter_approved().order_by("-date_posted")\
                .prefetch_related("author").prefetch_related("author__profile")

        # Basic + username (user posts)
        username = self.kwargs.get("username")
        if username:
            result = result.filter(author__username=username)

        # Basic + search string (search by post title and author)
        search_str = self.request.GET.get("q")
        if search_str:
            result = result.filter(Q(title__icontains=search_str) |
                                   Q(author__username__icontains=search_str))

        # Basic + posts date
        date = self.kwargs.get("date")
        if date:
            result = result.filter(date_posted=date)

        return result


class PostDetailView(LoginRequiredMixin, CreateView):
    """
    Post details
    """

    template_name = "blog/post_detail.html"
    form_class = PostStatusForm

    def get(self, request, *args, **kwargs):
        post = Post.objects.filter(slug=self.kwargs.get("slug")) \
            .prefetch_related("author").prefetch_related("author__profile").first()

        comment_id = request.GET.get("comment")
        if comment_id:
            # Edit comment
            comment = get_object_or_404(Comment, id=comment_id)
            comment_form = CommentForm(instance=comment)
        else:
            # New comment
            comment_form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by("-date_posted") \
            .prefetch_related("author").prefetch_related("author__profile")

        context = {
            "post": post,
            "comments": comments,
            "form": self.form_class(instance=post),
            "comment_form": comment_form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs.get("slug"))

        # Only admin users can change a post status
        if not request.user.is_staff:
            return redirect(post.get_absolute_url())

        form = self.form_class(request.POST)
        if form.is_valid():
            post.status = form.cleaned_data["status"]
            post.save()

        return redirect(post.get_absolute_url())


class CommentView(LoginRequiredMixin, CreateView):
    """
    Edit or create post comment
    """

    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs.get("slug"))

        comment_form = self.form_class(request.POST)
        if comment_form.is_valid():
            if comment_form.cleaned_data["id"]:
                # Edit an existing comment
                new_comment = get_object_or_404(Comment, id=comment_form.cleaned_data["id"])
            else:
                # New comment
                new_comment = Comment()
                new_comment.post = post
                new_comment.author = self.request.user

            new_comment.content = comment_form.cleaned_data["content"]
            # Notify user about a new comment (see signals)
            new_comment.save()

        return redirect(post.get_absolute_url())


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete post comment
    """

    model = Comment

    def post(self, request, *args, **kwargs):
        """
        Post comment can be deleted only by user who created it or admin user
        """
        comment = self.get_object()

        if self.request.user == comment.author or self.request.user.is_staff:
            comment.delete()

        return redirect(comment.post.get_absolute_url())


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    New post
    """

    model = Post
    fields = ["title", "content"]
    template_name = "blog/new_post.html"

    def post(self, request, *args, **kwargs):
        data = request.POST
        post = Post()
        post.title = data.get("title").strip()
        post.content = data.get("content")

        if post.title and post.content:
            user = self.request.user
            # Set post status (see signals)
            post.author = user
            post.save()

            return redirect(post.get_absolute_url())

        return redirect("blog:new-post")


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update post
    """

    model = Post
    fields = ["title", "content"]
    template_name = "blog/new_post.html"

    def form_valid(self, form):
        # Update date
        form.instance.date_posted = timezone.now
        return super().form_valid(form)

    def test_func(self):
        """
        Post can be updated only by user who created it or admin user
        """
        post = self.get_object()

        if self.request.user == post.author or self.request.user.is_staff:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete post
    """

    model = Post
    success_url = "/"

    def test_func(self):
        """
        Post can be deleted only by user who created it or admin user
        """
        post = self.get_object()

        if self.request.user == post.author or self.request.user.is_staff:
            return True
        return False


def e_handler404(request, exception):
    """
    404 Error handler
    """
    return render(request, 'blog/error404.html', status=404)


def e_handler500(request):
    """
    500 Error handler
    """
    return render(request, 'blog/error500.html', status=500)


def csrf_failure(request, exception):
    """
    CSRF token error
    """
    return render(request, 'blog/error403.html', status=403)
