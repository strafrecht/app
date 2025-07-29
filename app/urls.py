from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

# from wagtailpolls.views.results2 import results2  # Temporarily disabled for Django 5.x compatibility
from core.views import exams, api_exams, newsletter_subscribe, newsletter_confirm

# from wagtailpolls.views.vote import vote  # Temporarily disabled for Django 5.x compatibility
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls  # Re-enabled for Wagtail 6.x
from birdsong.urls import urlpatterns as birdsong_urls  # Re-enabled with forked wagtail-birdsong

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
    path('cms/autocomplete/', include(autocomplete_admin_urls)),  # Re-enabled for Wagtail 6.x
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

    path('mail/', include(birdsong_urls)),  # Re-enabled with forked wagtail-birdsong
    path('mail/subscribe', newsletter_subscribe, name='newsletter_subscribe'),
    path('mail/confirm/<str:hashed_email>/<str:email>',   newsletter_confirm,   name='newsletter_confirm'),
    path('', include('pwa.urls')),

    path('comments/', include('django_comments_xtd.urls')),  # Re-enabled with django-comments-xtd 2.10.7

    # re_path(r'^vote/(?P<poll_pk>.*)/$', vote, name='wagtailpolls_vote'),  # Temporarily disabled for Django 5.x compatibility

    # re_path(r'^results2/(?P<poll_pk>.*)/$', results2, name='wagtailpolls_results_2'),  # Temporarily disabled for Django 5.x compatibility
    path('problemfelder/', include('wiki.urls')),
    path('', include(wagtail_urls)),
    # path('avatar/', include('avatar.urls')),  # Temporarily disabled until avatar app is re-enabled

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Debug toolbar disabled - uncomment to enable
# if True and settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
