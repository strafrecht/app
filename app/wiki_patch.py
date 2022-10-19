def wiki_can_moderate(article, user):
    return user.is_superuser

def patch_wiki():
    """
    Monkey patch django-wiki
    """
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

    # add review message to user
    from django.contrib import messages
    from django.utils.translation import gettext as _
    from wiki import models
    from wiki.views.article import Edit, Create

    def edit_form_valid(self, form):
        result = self.original_form_valid(form)
        if not self.request.user.is_superuser:
            messages.success(
                self.request, _("The new revision will be reviewed and published by the moderators.")
            )
        return result

    Edit.original_form_valid = Edit.form_valid
    Edit.form_valid = edit_form_valid

    def create_form_valid(self, form):
        result = self.original_form_valid(form)
        if not self.request.user.is_superuser:
            messages.success(
                self.request, _("The new page will be reviewed and published by the moderators.")
            )
        return result

    Create.original_form_valid = Create.form_valid
    Create.form_valid = create_form_valid

    # overwrite str method
    from wiki.models.article import ArticleRevision

    def ar_str(self):
        return "%s (%d)" % (self.title, self.id)

    ArticleRevision.__str__ = ar_str

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

    if not self.id:
        # new article: set other_read, so only admin can access new wiki page
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
            message = "New wiki page: %s" % self.get_absolute_url()
        else:
            message = "Wiki page update: %s" % self.get_absolute_url()
        Submission.objects.create(article_revision=new_revision, submitted_by=new_revision.user, message=message)

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
    print(content)
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
