def wiki_can_moderate(article, user):
    return user.is_superuser

def patch_wiki():
    """
    Monkey patch django-wiki
    """
    # bugfix: add translation to password fields
    from django import forms
    from django.utils.translation import gettext_lazy as _
    from wiki import forms_account_handling
    class PatchedUserUpdateForm(forms_account_handling.UserUpdateForm):
        password1 = forms.CharField(
            label=_("New password"), widget=forms.PasswordInput(), required=False
        )
        password2 = forms.CharField(
            label=_("Confirm password"), widget=forms.PasswordInput(), required=False
        )
    forms_account_handling.UserUpdateForm = PatchedUserUpdateForm

    # bugfix: SHOW_MAX_CHILDREN is ignored in django-wiki
    from wiki.views.mixins import ArticleMixin
    ArticleMixin.get_context_data = get_context_data

    # don't publish pages edited/added by users
    from wiki.models.article import Article
    Article.add_revision = add_revision

    # fix mergeview get method
    from wiki.views.article import MergeView
    MergeView.get = fixed_mergeview_get

    # deny access to not superusers
    import wrapt
    from django.http import HttpResponseForbidden

    @wrapt.decorator
    def is_superuser(wrapped, instance, args, kwargs):
        if instance.request.user.is_superuser:
            return wrapped(*args, **kwargs)
        else:
            return HttpResponseForbidden("Forbidden")

    # allow only access from moderators to preview
    from wiki.views.article import Preview
    Preview.dispatch = is_superuser(Preview.dispatch)

    # allow only access from moderators to changerevisionview
    from wiki.views.article import ChangeRevisionView
    ChangeRevisionView.dispatch = is_superuser(ChangeRevisionView.dispatch)

    # allow only access from moderators to history
    from wiki.views.article import History
    History.dispatch = is_superuser(History.dispatch)

    # allow only access from moderators to move
    from wiki.views.article import Move
    Move.dispatch = is_superuser(Move.dispatch)

    # allow only access from moderators to settings
    from wiki.views.article import Settings
    Settings.dispatch = is_superuser(Settings.dispatch)

    # add review message to user
    from django.contrib import messages
    from django.utils.translation import gettext as _
    from wiki import models
    from wiki.views.article import Edit, Create

    def edit_form_valid(self, form):
        result = self.original_form_valid(form)
        if not self.request.user.is_superuser:
            if self.urlpath:
                messages.success(
                    self.request, _("Ihre Überarbeitung wird von unserem Team überprüft.")
                )
        return result

    Edit.original_form_valid = Edit.form_valid
    Edit.form_valid = edit_form_valid

    def create_form_valid(self, form):
        from django.urls import reverse
        from django.shortcuts import redirect
        try:
            self.newpath = models.URLPath._create_urlpath_from_request(
                self.request,
                self.article,
                self.urlpath,
                form.cleaned_data["slug"],
                form.cleaned_data["title"],
                form.cleaned_data["content"],
                form.cleaned_data["summary"],
            )
            messages.success(
                self.request,
                _("New article '%s' created.")
                % self.newpath.article.current_revision.title,
            )
            if not self.request.user.is_superuser:
                messages.success(
                    self.request, _("Ihre neue Seite wird von unserem Team überprüft.")
                )
        # TODO: Handle individual exceptions better and give good feedback.
        except Exception as e:
            log.exception("Exception creating article.")
            if self.request.user.is_superuser:
                messages.error(
                    self.request,
                    _("There was an error creating this article: %s") % str(e),
                )
            else:
                messages.error(
                    self.request, _("There was an error creating this article.")
                )
            return redirect("wiki:get", "")

        if self.request.user.is_superuser:
            return self.get_success_url()
        else:
            # redirect other users to parent page
            parent = reverse(
                "wiki:get",
                kwargs={"article_id": self.urlpath.article.id},
            )
            return redirect(parent)

    Create.form_valid = create_form_valid

    # overwrite str method
    from wiki.models.article import ArticleRevision

    def ar_str(self):
        return "%s (%d)" % (self.title, self.id)

    ArticleRevision.__str__ = ar_str

def get_context_data(self, **kwargs):
    from wiki.core.plugins import registry

    kwargs["urlpath"] = self.urlpath
    kwargs["article"] = self.article
    kwargs["article_tabs"] = registry.get_article_tabs()
    kwargs["children_slice"] = self.children_slice
    kwargs["children_slice_more"] = len(self.children_slice) > 20
    kwargs["plugins"] = registry.get_plugins()
    return kwargs

def add_revision(self, new_revision, save=True):
    """
    Sets the properties of a revision and ensures its the current
    revision.
    """
    # ArticleRevision not defined. Sometimes?
    from wiki.models.article import ArticleRevision
    from core.models import Submission

    assert self.id or save, (
        "Article.add_revision: Sorry, you cannot add a"
        "revision to an article that has not been saved "
        "without using save=True"
    )
    is_superuser = new_revision.user.is_superuser if new_revision.user else False
    new_article = not self.id

    # new article: set other_read and locked, so only admin can access new wiki page
    if new_article:
        new_revision.locked = not is_superuser
        self.other_read = is_superuser
        self.save()
    revisions = self.articlerevision_set.all()
    try:
        new_revision.revision_number = revisions.latest().revision_number + 1
    except ArticleRevision.DoesNotExist:
        new_revision.revision_number = 0

    new_revision.article = self
    new_revision.previous_revision = self.current_revision
    if save:
        new_revision.clean()
        new_revision.save()
    # set only the current edition if user is superuser
    if is_superuser:
        self.current_revision = new_revision
    if save:
        self.save()

    # create submission for admins
    if not is_superuser:
        if new_article:
            message = "Neue Wiki Seite"
        else:
            message = "Wiki Update"
        url = self.get_absolute_url() + "_history/"
        Submission.objects.create(content_object=new_revision,
                                  submitted_by=new_revision.user,
                                  message=message,
                                  url=url)

def fixed_mergeview_get(self, request, article, revision_id, *args, **kwargs):
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from django.shortcuts import render
    from django.shortcuts import redirect
    from django.utils.translation import gettext as _
    from wiki import models
    from wiki.core.diff import simple_merge

    revision = get_object_or_404(
        models.ArticleRevision, article=article, id=revision_id
    )

    current_text = (
        article.current_revision.content if article.current_revision else ""
    )
    new_text = revision.content

    content = simple_merge(current_text, new_text)
    # Save new revision
    if not self.preview:
        old_revision = article.current_revision

        if revision.deleted:
            c = {
                "error_msg": _("You cannot merge with a deleted revision"),
                "article": article,
                "urlpath": self.urlpath,
            }
            return render(request, self.template_error_name, context=c)

        new_revision = models.ArticleRevision()
        new_revision.inherit_predecessor(article)
        # following line was missing (user was not set ...)
        new_revision.set_from_request(self.request)
        new_revision.deleted = False
        new_revision.locked = False
        new_revision.title = article.current_revision.title
        new_revision.content = content
        new_revision.automatic_log = _(
            "Merge between revision #%(r1)d and revision #%(r2)d"
        ) % {"r1": revision.revision_number, "r2": old_revision.revision_number}
        article.add_revision(new_revision, save=True)

        old_revision.simpleplugin_set.all().update(article_revision=new_revision)
        revision.simpleplugin_set.all().update(article_revision=new_revision)

        messages.success(
            request,
            _(
                "A new revision was created: Merge between revision #%(r1)d and revision #%(r2)d"
            )
            % {"r1": revision.revision_number, "r2": old_revision.revision_number},
        )
        if self.urlpath:
            return redirect("wiki:edit", path=self.urlpath.path)
        else:
            return redirect("wiki:edit", article_id=article.id)

    c = {
        "article": article,
        "title": article.current_revision.title,
        "revision": None,
        "merge1": revision,
        "merge2": article.current_revision,
        "merge": True,
        "content": content,
    }
    return render(request, self.template_name, c)
