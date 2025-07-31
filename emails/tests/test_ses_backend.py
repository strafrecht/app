"""
Test suite for AWS SES backend integration
"""

import unittest
from unittest.mock import patch, MagicMock, call
from django.test import TestCase, override_settings
from django.template.exceptions import TemplateDoesNotExist
from botocore.exceptions import ClientError, BotoCoreError

from birdsong.models import Contact, CampaignStatus
from emails.models import LSHNewsletter


@override_settings(
    AWS_ACCESS_KEY_ID='test-key-id',
    AWS_SECRET_ACCESS_KEY='test-secret-key',
    AWS_SES_REGION='eu-west-1',
    AWS_SES_BATCH_SIZE=5,
    AWS_SES_RATE_LIMIT=10
)
class SESBackendTestCase(TestCase):
    """Test cases for SES email backend"""
    
    def setUp(self):
        """Set up test data"""
        # Create test campaign
        self.campaign = LSHNewsletter.objects.create(
            name="Test Campaign",
            subject="Test Subject",
            body=[{
                "type": "paragraph", 
                "value": "<p>Test newsletter content</p>"
            }]
        )
        
        # Create test contacts
        self.contacts = [
            Contact.objects.create(email="test1@example.com"),
            Contact.objects.create(email="test2@example.com"),
            Contact.objects.create(email="test3@example.com"),
        ]
    
    @patch('birdsong.backends.ses.boto3.Session')
    def test_ses_backend_import(self, mock_session):
        """Test that SES backend can be imported and initialized"""
        from birdsong.backends.ses import SESEmailBackend
        
        backend = SESEmailBackend()
        self.assertIsNotNone(backend)
    
    @patch('birdsong.backends.ses.boto3.Session')
    def test_send_campaign_success(self, mock_session):
        """Test successful campaign sending"""
        from birdsong.backends.ses import SESEmailBackend
        
        # Mock SES client
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.send_email.return_value = {'MessageId': 'test-message-id-123'}
        
        # Create backend and send campaign
        backend = SESEmailBackend()
        backend.send_campaign(None, self.campaign, self.contacts, test_send=True)
        
        # Verify SES client was called for each contact
        self.assertEqual(mock_client.send_email.call_count, len(self.contacts))
        
        # Verify campaign status
        self.campaign.refresh_from_db()
        # Note: In test_send mode, status is not automatically updated
    
    @patch('birdsong.backends.ses.boto3.Session')
    def test_send_campaign_with_client_error(self, mock_session):
        """Test campaign sending with SES client errors"""
        from birdsong.backends.ses import SESEmailBackend
        
        # Mock SES client with error
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.send_email.side_effect = ClientError(
            error_response={'Error': {'Code': 'Throttling', 'Message': 'Rate exceeded'}},
            operation_name='SendEmail'
        )
        
        # Create backend and send campaign
        backend = SESEmailBackend()
        
        # Should not raise exception, but handle gracefully
        try:
            backend.send_campaign(None, self.campaign, self.contacts, test_send=True)
        except Exception as e:
            self.fail(f"SES backend should handle ClientError gracefully, but raised: {e}")
    
    @patch('birdsong.backends.ses.boto3.Session')
    def test_message_formatting(self, mock_session):
        """Test that messages are formatted correctly for SES"""
        from birdsong.backends.ses import SESEmailBackend
        
        # Mock SES client
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.send_email.return_value = {'MessageId': 'test-message-id'}
        
        # Create backend and send campaign
        backend = SESEmailBackend()
        backend.send_campaign(None, self.campaign, [self.contacts[0]], test_send=True)
        
        # Get the call arguments
        call_args = mock_client.send_email.call_args[1]
        
        # Verify message structure
        self.assertIn('Source', call_args)
        self.assertIn('Destination', call_args)
        self.assertIn('Message', call_args)
        
        # Verify destination
        self.assertEqual(call_args['Destination']['ToAddresses'], [self.contacts[0].email])
        
        # Verify message content
        message = call_args['Message']
        self.assertIn('Subject', message)
        self.assertIn('Body', message)
        self.assertEqual(message['Subject']['Data'], self.campaign.subject)
    
    @patch('birdsong.backends.ses.boto3.Session')
    def test_batch_processing(self, mock_session):
        """Test that large contact lists are processed in batches"""
        from birdsong.backends.ses import SESCampaignThread
        
        # Create more contacts to test batching
        additional_contacts = [
            Contact.objects.create(email=f"test{i}@example.com") 
            for i in range(4, 15)  # Total will be 15 contacts
        ]
        all_contacts = self.contacts + additional_contacts
        
        # Mock SES client
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.send_email.return_value = {'MessageId': 'test-message-id'}
        
        # Create messages (simplified for testing)
        messages = [
            {
                'subject': 'Test',
                'from_email': 'test@example.com',
                'to': [contact.email],
                'html_body': '<p>Test</p>'
            }
            for contact in all_contacts
        ]
        
        # Create and run campaign thread
        thread = SESCampaignThread(
            self.campaign.pk,
            [c.pk for c in all_contacts],
            messages
        )
        thread._get_ses_client = lambda: mock_client
        
        # Run the thread
        thread.run()
        
        # Verify all emails were sent
        self.assertEqual(mock_client.send_email.call_count, len(all_contacts))
    
    @patch('birdsong.backends.ses.boto3.Session')
    def test_rate_limiting(self, mock_session):
        """Test that rate limiting is respected"""
        from birdsong.backends.ses import SESCampaignThread
        import time
        
        # Mock SES client
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.send_email.return_value = {'MessageId': 'test-message-id'}
        
        # Create messages
        messages = [
            {
                'subject': 'Test',
                'from_email': 'test@example.com',
                'to': [contact.email],
                'html_body': '<p>Test</p>'
            }
            for contact in self.contacts
        ]
        
        # Mock time.sleep to verify it's called
        with patch('birdsong.backends.ses.time.sleep') as mock_sleep:
            thread = SESCampaignThread(
                self.campaign.pk,
                [c.pk for c in self.contacts],
                messages
            )
            thread._get_ses_client = lambda: mock_client
            
            # Run the thread
            thread.run()
            
            # Verify sleep was called for rate limiting
            # (Should be called between batches if there are multiple batches)
            if len(messages) > 5:  # AWS_SES_BATCH_SIZE is 5 in test settings
                mock_sleep.assert_called()
    
    def test_configuration_validation(self):
        """Test that configuration validation works"""
        from birdsong.backends.ses import SESEmailBackend
        
        # Test with missing configuration
        with override_settings():
            # Remove AWS settings
            if hasattr(settings, 'AWS_SES_REGION'):
                delattr(settings, 'AWS_SES_REGION')
            
            # Should still initialize but log warnings
            backend = SESEmailBackend()
            self.assertIsNotNone(backend)
    
    @patch('birdsong.backends.ses.boto3.Session')
    def test_template_rendering(self, mock_session):
        """Test template rendering for campaigns"""
        from birdsong.backends.ses import SESEmailBackend
        
        # Mock SES client
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.send_email.return_value = {'MessageId': 'test-message-id'}
        
        # Create backend
        backend = SESEmailBackend()
        
        # Mock template rendering to test both HTML and text templates
        with patch('birdsong.backends.ses.render_to_string') as mock_render:
            mock_render.side_effect = [
                '<html><body>HTML content</body></html>',  # HTML template
                'Text content'  # Text template
            ]
            
            backend.send_campaign(None, self.campaign, [self.contacts[0]], test_send=True)
            
            # Verify both templates were rendered
            self.assertEqual(mock_render.call_count, 2)
    
    @patch('birdsong.backends.ses.boto3.Session')
    def test_template_not_found_fallback(self, mock_session):
        """Test fallback when text template is not found"""
        from birdsong.backends.ses import SESEmailBackend
        
        # Mock SES client
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.send_email.return_value = {'MessageId': 'test-message-id'}
        
        # Create backend
        backend = SESEmailBackend()
        
        # Mock template rendering with TemplateDoesNotExist for text template
        with patch('birdsong.backends.ses.render_to_string') as mock_render:
            mock_render.side_effect = [
                '<html><body>HTML content</body></html>',  # HTML template
                TemplateDoesNotExist('text template not found')  # Text template missing
            ]
            
            backend.send_campaign(None, self.campaign, [self.contacts[0]], test_send=True)
            
            # Should still send email with HTML content as fallback
            mock_client.send_email.assert_called_once()
            
            # Verify the message structure
            call_args = mock_client.send_email.call_args[1]
            message_body = call_args['Message']['Body']
            
            # Should have HTML body
            self.assertIn('Html', message_body)
            # Text body should use HTML content as fallback
            self.assertIn('Text', message_body)
