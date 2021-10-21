from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User

from itertools import groupby

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Collection
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

import pages 

class PeopleIndexPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Aktuelle Mitarbeiter*innen-Seite"
        
    subtitle = models.CharField(max_length=255, null=True, blank=True)

    content_panels = Page.content_panels + [                                          
        FieldPanel('subtitle'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        staff = People.objects.filter(status='current')

        context['head'] = staff.filter(role='chairholder')
        context['office'] = staff.filter(role='office-management')
        context['academic'] = staff.filter(
            Q(role='academic-staff-male') | Q(role='academic-staff-female') | Q(role='academic-assistant')
        )
        context['student'] = staff.filter(role='student-assistant')
        return context

    @route('(?P<person>\d+)/$', name="person")
    def person_page(self, request, person):
        context = super().get_context(request)
        person = People.objects.get(id=person)

        articles = pages.models.NewsArticlePage.objects.filter(live=True).filter(owner__id=person.id).order_by('-date')

        years = []
        keys = []

        for key, group in groupby(articles, lambda x: x.date.year):
            years.append({"year": key, "articles": list(group)})
            keys.append(key)

        context['groups'] = years
        context['person'] = person
        return render(request, "pages/person_page.html", context)
    
class FormerPeopleIndexPage(Page):
    class Meta:
        verbose_name = "Ehemalige Mitarbeiter*innen-Seite"
        
    def get_context(self, request):
        context = super().get_context(request)
        formerstaff = People.objects.filter(status='former')

        context['former_staff'] = formerstaff
        return context

@register_snippet
class People(models.Model):
    STATUS_CHOICES = [
        ('former', 'Ehemalig'),
        ('current', 'Aktuell'),
    ]

    ROLE_CHOICES = [
        ('chairholder', 'Lehstuhlinhaber'),
        ('office-management', 'Office Management'),
        ('academic-staff-male', 'Wiss. Mitarbeiter'),
        ('academic-staff-female', 'Wiss. Mitarbeiterin'),
        ('academic-assistant', 'Wiss. Hilfskraft'),
        ('student-assistant', 'Stud. Hilfskraft'),
        ('jurcoach-law-team', 'Jurcoach Jura-Team'),
        ('jurcoach-evaluation-team', 'Jurcoach Evaluations-Team'),
        ('jurcoach-web-team', 'Jurcoach Informatik-Team'),
        ('webmaster', 'Webmaster'),
        ('associate-professor', 'Privatdozent'),
    ]

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Verknüpfung mit Nutzer*innen-Account'
    )
    first_name = models.CharField("Vorname", max_length=255)
    last_name = models.CharField("Nachname", max_length=255)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='former',
        max_length=255,
        blank=True,
    )
    role = models.CharField(
        'Rolle',
        choices=ROLE_CHOICES,
        max_length=255,
        blank=True,
    )
    telephone = models.CharField("Telefonnummer", max_length=255, blank=True)
    email = models.CharField("Mailadresse", max_length=255, blank=True)
    room = models.CharField("Raumnummer", max_length=255, blank=True)
    description = RichTextField(blank=True, verbose_name='Beschreibung/Weitere Informationen')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Profilbild'
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('user', classname="col-12"),
            ]),
            FieldRowPanel([
                FieldPanel('first_name', classname="col-6"),
                FieldPanel('last_name', classname="col-6"),
            ], "Name"),
            FieldRowPanel([
                FieldPanel('telephone', classname="col-4"),
                FieldPanel('email', classname="col-4"),
            ], "Contact"),
            FieldRowPanel([
                FieldPanel('status', classname="col-6"),
                FieldPanel('role', classname="col-6"),
            ]),
            FieldRowPanel([
                FieldPanel('room', classname="col-4"),
            ], "Room"),
        ], "Information"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('description', classname="col-12"),
            ]),
        ], "Weitere Informationen"),
        ImageChooserPanel('image')
    ]

    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    @property
    def thumb_image(self):
        try:
            return self.image.get_rendition('fill-120x120').img_tag()
        except:
            return ''

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Personen'
