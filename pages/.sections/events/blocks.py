from wagtail.core import blocks

class EventsListAll(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/events_list.html'

    def get_context(self, *a, **kw):
        ctx = super().get_context(*a, **kw)
        ctx['events'] = Events.objects.all()
        return ctx