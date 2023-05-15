# patch wagtail-birdsong to prepare and send mails in background

import logging
from smtplib import SMTPException
from threading import Thread

from django.db import close_old_connections, transaction
from django.template.loader import render_to_string
from django.utils import timezone

from birdsong.models import Campaign, CampaignStatus, Contact
from birdsong.utils import send_mass_html_mail

from birdsong.backends import BaseEmailBackend
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

class SendCampaignThread(Thread):
    def __init__(self, campaign_pk, contact_pks, messages):
        super().__init__()
        self.campaign_pk = campaign_pk
        self.contact_pks = contact_pks
        self.messages = messages

    def run(self):
        try:
            logger.info(f"Sending {len(self.messages)} emails")
            send_mass_html_mail(self.messages)
            logger.info("Sending finished")
            with transaction.atomic():
                Campaign.objects.filter(pk=self.campaign_pk).update(
                    status=CampaignStatus.SENT,
                    sent_date=timezone.now(),
                )
                fresh_contacts = Contact.objects.filter(
                    pk__in=self.contact_pks)
                Campaign.objects.get(
                    pk=self.campaign_pk).receipts.add(*fresh_contacts)
        except SMTPException:
            logger.exception(f"Problem sending campaign: {self.campaign_pk}")
            self.campaign.status = CampaignStatus.FAILED
        finally:
            close_old_connections()

class SMTPBackgroundTread(Thread):
    def __init__(self, from_email, reply_to, request, campaign, contact_pks, test_send):
        super().__init__()
        self.from_email = from_email
        self.reply_to = reply_to
        self.request = request
        self.campaign = campaign
        self.contacts = Contact.objects.filter(pk__in=contact_pks)
        self.test_send = test_send

    def run(self):
        messages = []
        logger.info(f"Preparing {len(self.contacts)} emails")
        for contact in self.contacts:
            logger.info(f"Preparing {contact.email}")
            content = render_to_string(
                self.campaign.get_template(self.request),
                self.campaign.get_context(self.request, contact),
            )
            messages.append({
                'subject': self.campaign.subject,
                'body': content,
                'from_email': self.from_email,
                'to': [contact.email],
                'reply_to': [self.reply_to],
            })
        logger.info(f"Preparing finished")
        if self.test_send:
            # Don't mark as complete, don't worry about threading
            send_mass_html_mail(messages)
        else:
            campaign_thread = SendCampaignThread(
                self.campaign.pk, [c.pk for c in self.contacts], messages)
            campaign_thread.start()


class SMTPBackgroundBackend(BaseEmailBackend):
    def send_campaign(self, request, campaign, contacts, test_send=False):
        background_thread = SMTPBackgroundTread(
            self.from_email, self.reply_to, request, campaign, [c.pk for c in contacts], test_send)
        background_thread.start()


logger = logging.getLogger(__name__)


def patch_birdsong():
    """
    Monkey patch wagtail-birdsong
    """

    from birdsong.options import CampaignAdmin
    CampaignAdmin.backend_class = SMTPBackgroundBackend
