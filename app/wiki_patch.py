def wiki_can_moderate(article, user):
    return user.is_superuser

def patch_wiki():
    """
    Monkey patch django-wiki
    """
    # don't publish pages edited/added by users
    from wiki.models.article import Article
    Article.add_revision = add_revision

    # allow only access from moderators to history
    from django.utils.decorators import method_decorator
    from wiki.decorators import get_article
    from wiki.views.article import History

    @method_decorator(get_article(can_read=True, can_moderate=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(History, self).dispatch(request, article, *args, **kwargs)

    History.dispatch = dispatch

    # add message to user
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

def add_revision(self, new_revision, save=True):
    """
    Sets the properties of a revision and ensures its the current
    revision.
    """
    # ArticleRevision not defined. Sometimes?
    from wiki.models.article import ArticleRevision

    assert self.id or save, (
        "Article.add_revision: Sorry, you cannot add a"
        "revision to an article that has not been saved "
        "without using save=True"
    )
    if not self.id:
        # new article: set other_read, so only admin can access new wiki page
        self.other_read = new_revision.user.is_superuser
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
    if new_revision.user.is_superuser:
        self.current_revision = new_revision
    if save:
        self.save()
