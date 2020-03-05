from secrets import token_hex
from django.contrib import admin
from blog.models import Post, Comment


class InlineComments(admin.TabularInline):
    """
     Edit comment related to a post in the post view
    """
    model = Comment
    extra = 0


class FilterPosts(admin.ModelAdmin):
    """
    Posts customization in the admin panel
    """
    inlines = [InlineComments]
    list_display = ("title", "author", "status", "date_posted")
    list_filter = ("status", "date_posted")
    list_editable = ("status", )
    search_fields = ("title__icontains", "author__username__icontains")
    # Default value for a slug field
    prepopulated_fields = {"slug": ("title", )}


class FilterComments(admin.ModelAdmin):
    """
    Comment customization in the admin panel
    """
    list_display = ("post", "author", "date_posted")
    list_filter = ("date_posted", )
    search_fields = ("post__title__icontains", "author__username__icontains")


admin.site.register(Post, FilterPosts)
admin.site.register(Comment, FilterComments)
