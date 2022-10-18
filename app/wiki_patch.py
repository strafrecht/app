def wiki_can_moderate(article, user):
    return user.is_superuser

def patch_wiki():
    """
    Monkey patch django-wiki
    """
    from wiki.models.article import Article, ArticleRevision
    Article.add_revision = add_revision

    from django.utils.decorators import method_decorator
    from wiki.decorators import get_article
    from wiki.views.article import History

    # allow only access from moderators
    @method_decorator(get_article(can_read=True, can_moderate=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(History, self).dispatch(request, article, *args, **kwargs)

    History.dispatch = dispatch


def add_revision(self, new_revision, save=True):
    """
    Sets the properties of a revision and ensures its the current
    revision.
    """
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
