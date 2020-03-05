"""mini_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from blog.views import e_handler404, e_handler500
from django.conf.urls.static import static
from django.conf.urls import url
from blog.views import PostListView


# Admin panel
admin.site.site_header = 'Mini Blog'
admin.site.site_title = _('Admin panel')
admin.site.index_title = _('Mini Blog Administrator')


handler404 = e_handler404
handler500 = e_handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='home'),
    # MiniBlog (Posts and Comments)
    path('post/', include('blog.urls')),
    # Users
    path('', include('users.urls')),
    # Confirm password reset
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    # Password reset complete
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    # Social accounts
    path('accounts/', include('allauth.urls')),
    # Change language
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
