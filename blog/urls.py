from django.urls import path
from blog.views import (
    PostListView, PostCreateView, PostDetailView,
    PostUpdateView, PostDeleteView, CommentView, CommentDeleteView
)


app_name = "blog"


urlpatterns = [
    # User posts
    path('user/<str:username>/', PostListView.as_view(), name='user-posts'),
    # Posts by date
    path('date/<str:date>/', PostListView.as_view(), name='date-posts'),
    # New post
    path('new/', PostCreateView.as_view(), name='new-post'),
    # All post
    path('<slug>/', PostDetailView.as_view(), name='post-detail'),
    # Update post
    path('<slug>/update/', PostUpdateView.as_view(), name='post-update'),
    # Delete post
    path('<slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # New comment
    path('comment/<slug>/new/', CommentView.as_view(), name='new-comment'),
    # Delete comment
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
]
