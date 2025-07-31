"""
Management command to test AWS SES integration
Usage: python manage.py test_ses --email your@email.com
"""

import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils import timezone
from birdsong.models import Contact
from emails.models import LSHNewsletter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test AWS SES integration by sending a test newsletter'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Email address to send test newsletter to'
        )
        parser.add_argument(
            '--backend',
            type=str,
            default=None,
            help='Backend class to use (default: from settings)'
        )
        parser.add_argument(
            '--create-campaign',
            action='store_true',
            help='Create a new test campaign instead of using existing'
        )

    def handle(self, *args, **options):
        email = options['email']
        backend_class_path = options['backend'] or getattr(
            settings, 'BIRDSONG_BACKEND_CLASS', 'birdsong.backends.smtp.SMTPEmailBackend'
        )
        
        self.stdout.write(f"Testing email backend: {backend_class_path}")
        
        try:
            # Import the backend class
            backend_class = import_string(backend_class_path)
            backend = backend_class()
            
            self.stdout.write(f"Successfully imported backend: {backend_class}")
            
        except ImportError as e:
            raise CommandError(f"Failed to import backend class '{backend_class_path}': {e}")
        
        # Create or get test contact
        contact, created = Contact.objects.get_or_create(email=email)
        if created:
            self.stdout.write(f"Created new contact: {email}")
        else:
            self.stdout.write(f"Using existing contact: {email}")
        
        # Create or get test campaign
        if options['create_campaign']:
            campaign = self._create_test_campaign()
            self.stdout.write(f"Created new test campaign: {campaign.name}")
        else:
            try:
                campaign = LSHNewsletter.objects.filter(name__icontains='test').first()
                if not campaign:
                    campaign = self._create_test_campaign()
                    self.stdout.write(f"No existing test campaign found, created: {campaign.name}")
                else:
                    self.stdout.write(f"Using existing campaign: {campaign.name}")
            except Exception as e:
                raise CommandError(f"Failed to get or create campaign: {e}")
        
        # Test the backend
        try:
            self.stdout.write("Sending test email...")
            
            # Send test email
            backend.send_campaign(
                request=None,
                campaign=campaign,
                contacts=[contact],
                test_send=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(f"✅ Test email sent successfully to {email}")
            )
            
            # If using SES backend, try to get some statistics
            if 'ses' in backend_class_path.lower():
                self._show_ses_statistics()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to send test email: {e}")
            )
            logger.exception("Test email sending failed")
            raise CommandError(f"Email sending failed: {e}")

    def _create_test_campaign(self):
        """Create a test campaign for SES testing"""

        campaign = LSHNewsletter.objects.create(
            name="SES Test Campaign",
            subject="AWS SES Integration Test",
            body=[
                {
                    "type": "paragraph",
                    "value": (
                        "<p>This is a test email to verify AWS SES integration.</p>"
                        "<p>If you receive this email, the SES backend is working correctly.</p>"
                        "<p>Test sent at: {}</p>".format(
                            timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                    )
                }
            ]
        )
        return campaign

    def _show_ses_statistics(self):
        """Show SES statistics if available"""
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            # Get SES client
            session = boto3.Session(
                aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
                aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
                region_name=getattr(settings, 'AWS_SES_REGION', 'eu-west-1')
            )
            ses_client = session.client('ses')
            
            # Get send quota
            quota = ses_client.get_send_quota()
            self.stdout.write("\n📊 SES Statistics:")
            self.stdout.write(f"  • Max 24 Hour Send: {quota['Max24HourSend']}")
            self.stdout.write(f"  • Max Send Rate: {quota['MaxSendRate']} emails/second")
            self.stdout.write(f"  • Sent Last 24h: {quota['SentLast24Hours']}")
            
            # Get send statistics
            stats = ses_client.get_send_statistics()
            if stats['SendDataPoints']:
                latest = stats['SendDataPoints'][-1]
                self.stdout.write(f"  • Recent Bounces: {latest.get('Bounces', 0)}")
                self.stdout.write(f"  • Recent Complaints: {latest.get('Complaints', 0)}")
                self.stdout.write(f"  • Recent Rejects: {latest.get('Rejects', 0)}")
            
        except ImportError:
            self.stdout.write("⚠️  boto3 not available, cannot show SES statistics")
        except ClientError as e:
            self.stdout.write(f"⚠️  Could not retrieve SES statistics: {e}")
        except Exception as e:
            self.stdout.write(f"⚠️  Error getting SES statistics: {e}")

    def _validate_ses_configuration(self):
        """Validate SES configuration"""
        required_settings = [
            'AWS_SES_REGION',
        ]
        
        missing_settings = []
        for setting in required_settings:
            if not hasattr(settings, setting):
                missing_settings.append(setting)
        
        if missing_settings:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  Missing SES settings: {', '.join(missing_settings)}"
                )
            )
        
        # Check for AWS credentials
        if not (hasattr(settings, 'AWS_ACCESS_KEY_ID') and hasattr(settings, 'AWS_SECRET_ACCESS_KEY')):
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  AWS credentials not found in settings. "
                    "Ensure they're available via IAM role or environment variables."
                )
            )
