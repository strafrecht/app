from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from core.views import exams, api_exams

from wagtailpolls.views.vote import vote
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls
from birdsong.urls import urlpatterns as birdsong_urls

urlpatterns = [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name='password_reset'),
    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),

    path('admin/', admin.site.urls),
    path('cms/autocomplete/', include(autocomplete_admin_urls)),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('search/', include('pages.urls')),

    path('profile/', include('profiles.urls')),
    path('jurcoach/klausurendatenbank/', exams, name='exams'),
    path('jurcoach/klausurendatenbank/api', api_exams, name='exams'),
    path('falltraining/', include('casetraining.urls')),
    path('tandemklausuren/', include('tandem_exams.urls')),

    path('notifications/', include('django_nyt.urls')),

    path('feedback/', include('feedback.urls')),

    path('flashcards/', include('flashcards.urls')),
    path('quiz/', include('quiz.urls')),
    path('run/', include('core.urls')),
    path('lehre/', include('core.urls')),

    path('mail/', include(birdsong_urls)),
    path('', include('pwa.urls')),

    path('comments/', include('django_comments_xtd.urls')),

    re_path(r'^vote/(?P<poll_pk>.*)/$', vote, name='wagtailpolls_vote'),

    path('problemfelder/', include('wiki.urls')),
    path('', include(wagtail_urls)),
    path('avatar/', include('avatar.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if True and settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
