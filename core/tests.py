from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import salted_hmac
from django.contrib.messages import get_messages
from django.conf import settings
from birdsong.models import Contact

from core.views import newsletter_confirm, newsletter_subscribe

class SubscriptionTest(TestCase):
    def test_subscribe(self):
        url = reverse('newsletter_subscribe')
        email = 'test@example.com'
        response = self.client.post(url, {'email': email})
        self.assertRedirects(response, '/archiv/lsh-newsletter/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=False)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Wir senden Dir eine Bestätigungs-E-Mail für die Anmeldung zu.')

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, [email])
        self.assertEqual(message.subject, 'Bestätigung der Anmeldung zum LSH-Newsletter')
        confirmation_url = reverse('newsletter_confirm', args=[salted_hmac(settings.SECRET_KEY, email.lower()).hexdigest(), email])
        self.assertIn(confirmation_url, message.body)

class ConfirmationTest(TestCase):
    def test_confirm(self):
        url = reverse('newsletter_confirm', args=[salted_hmac(settings.SECRET_KEY, 'test@example.com'.lower()).hexdigest(), 'test@example.com'])
        with self.assertRaises(Contact.DoesNotExist):
            Contact.objects.get(email="test@example.com")
        response = self.client.post(url)
        self.assertRedirects(response, '/archiv/lsh-newsletter/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=False)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Du wurdest für den LSH-Newsletter eingetragen.')
        self.assertEqual("test@example.com", Contact.objects.get(email="test@example.com").email)

    def test_invalid_confirm(self):
        url = reverse('newsletter_confirm', args=['invalid_hash', 'test@example.com'])
        response = self.client.post(url)
        self.assertRedirects(response, '/archiv/lsh-newsletter/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=False)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Der Bestätigungslink ist nicht korrekt.')
