from django.contrib import admin
from users.models import UserGroup, Profile


class FilterUserGroups(admin.ModelAdmin):
    """
    User group customization in the admin panel
    """
    list_display = ("name", "pre_moderation")
    list_filter = ("name", "pre_moderation")
    search_fields = ("name__icontains", )


class FilterProfiles(admin.ModelAdmin):
    """
    User profile customization in the admin panel
    """
    list_display = ("user", "email_confirmed", "user_group")
    list_filter = ("email_confirmed", "user_group")
    readonly_fields = ("image",)
    list_editable = ("email_confirmed", "user_group")
    search_fields = ("user__username__icontains",)


admin.site.register(UserGroup, FilterUserGroups)
admin.site.register(Profile, FilterProfiles)
