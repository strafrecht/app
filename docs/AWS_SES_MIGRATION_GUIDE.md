# AWS SES Migration Guide for Strafrecht-Online Newsletter System

## Overview

This guide provides step-by-step instructions for migrating from the current SMTP-based newsletter system to AWS Simple Email Service (SES) for improved deliverability, scalability, and monitoring.

## Prerequisites

### AWS Account Setup
1. **AWS Account**: Ensure you have an AWS account with appropriate permissions
2. **IAM User**: Create dedicated IAM user for SES with minimal required permissions
3. **Domain Ownership**: Verify ownership of `strafrecht-online.org`

### Required IAM Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail",
                "ses:SendBulkTemplatedEmail",
                "ses:GetSendQuota",
                "ses:GetSendStatistics",
                "ses:ListVerifiedEmailAddresses",
                "ses:ListIdentities"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

## Phase 1: AWS SES Configuration

### Step 1: Domain Verification

1. **Login to AWS Console** → Navigate to SES service
2. **Verify Domain**:
   - Go to "Verified identities" → "Create identity"
   - Select "Domain" and enter `strafrecht-online.org`
   - Choose "Easy DKIM" for authentication
3. **Add DNS Records**: Add the provided DNS records to your domain:
   ```
   Type: TXT
   Name: _amazonses.strafrecht-online.org
   Value: [AWS-provided verification string]
   
   Type: CNAME (for DKIM - 3 records)
   Name: [dkim-selector]._domainkey.strafrecht-online.org
   Value: [AWS-provided DKIM value]
   ```

### Step 2: Request Production Access

1. **Navigate to Account Dashboard** in SES console
2. **Request Production Access**:
   - Click "Request production access"
   - Fill out the form with:
     - **Use case**: Newsletter and transactional emails for legal education platform
     - **Website URL**: https://strafrecht-online.org
     - **Expected volume**: [Your current newsletter volume]
     - **Bounce/complaint handling**: Describe your subscription management

### Step 3: Configure Bounce and Complaint Handling

1. **Create SNS Topics**:
   ```bash
   aws sns create-topic --name ses-bounces-strafrecht
   aws sns create-topic --name ses-complaints-strafrecht
   ```

2. **Configure SES Notifications**:
   - Go to verified domain → "Notifications"
   - Set bounce and complaint topics to the created SNS topics

## Phase 2: Application Configuration

### Step 1: Install Dependencies

Add to `requirements/common.txt`:
```
boto3>=1.26.0
botocore>=1.29.0
```

Install dependencies:
```bash
pip install boto3 botocore
```

### Step 2: Environment Configuration

Update `app/vars.py` (or your environment configuration):

```python
# AWS SES Configuration
AWS_ACCESS_KEY_ID = "your-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-secret-access-key"
AWS_SES_REGION = "eu-west-1"  # Choose appropriate region
AWS_SES_BATCH_SIZE = 10       # Emails per batch
AWS_SES_RATE_LIMIT = 14       # Emails per second (adjust based on your limits)

# SES-specific settings
BIRDSONG_BACKEND_CLASS = "birdsong.backends.ses.SESEmailBackend"
BIRDSONG_FALLBACK_BACKEND = "birdsong.backends.smtp.SMTPEmailBackend"  # Fallback option
```

### Step 3: Settings Updates

Update `app/settings.py`:

```python
# Email Backend Configuration
if DEBUG:
    # Development - use mailcatcher
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = "localhost"
    EMAIL_PORT = "1025"
    BIRDSONG_BACKEND_CLASS = "birdsong.backends.smtp.SMTPEmailBackend"
else:
    # Production - use AWS SES
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Keep for non-newsletter emails
    
    # AWS SES Configuration
    AWS_ACCESS_KEY_ID = vars.vars.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = vars.vars.get("AWS_SECRET_ACCESS_KEY")
    AWS_SES_REGION = vars.vars.get("AWS_SES_REGION", "eu-west-1")
    AWS_SES_BATCH_SIZE = vars.vars.get("AWS_SES_BATCH_SIZE", 10)
    AWS_SES_RATE_LIMIT = vars.vars.get("AWS_SES_RATE_LIMIT", 14)
    
    # Birdsong SES Backend
    BIRDSONG_BACKEND_CLASS = vars.vars.get("BIRDSONG_BACKEND_CLASS", "birdsong.backends.ses.SESEmailBackend")

# Enhanced logging for SES
LOGGING['loggers']['birdsong.backends.ses'] = {
    'handlers': ['file'],
    'level': 'INFO',
    'propagate': True,
}
```

### Step 4: Update Birdsong Configuration

Update `emails/wagtail_hooks.py`:

```python
from django.conf import settings
from django.utils.module_loading import import_string

class LSHNewsletterAdmin(CampaignAdmin):
    model = LSHNewsletter
    menu_label = 'LSH'
    menu_icon = 'mail'
    contact_class = Contact
    contact_filter_class = ContactFilter
    
    # Use configured backend class
    backend_class = import_string(getattr(settings, 'BIRDSONG_BACKEND_CLASS', 'birdsong.backends.smtp.SMTPEmailBackend'))
```

## Phase 3: Testing Strategy

### Step 1: Unit Testing

Create test file `tests/test_ses_backend.py`:

```python
import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from birdsong.backends.ses import SESEmailBackend
from emails.models import LSHNewsletter
from birdsong.models import Contact

@override_settings(
    AWS_ACCESS_KEY_ID='test-key',
    AWS_SECRET_ACCESS_KEY='test-secret',
    AWS_SES_REGION='eu-west-1'
)
class SESBackendTestCase(TestCase):
    def setUp(self):
        self.backend = SESEmailBackend()
        self.campaign = LSHNewsletter.objects.create(
            name="Test Campaign",
            subject="Test Subject",
            body=[{"type": "paragraph", "value": "Test content"}]
        )
        self.contact = Contact.objects.create(email="test@example.com")
    
    @patch('boto3.Session')
    def test_send_campaign(self, mock_session):
        # Mock SES client
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.send_email.return_value = {'MessageId': 'test-message-id'}
        
        # Test campaign sending
        self.backend.send_campaign(None, self.campaign, [self.contact], test_send=True)
        
        # Verify SES client was called
        mock_client.send_email.assert_called_once()
```

### Step 2: Integration Testing

1. **Sandbox Testing**: Use SES sandbox mode for initial testing
2. **Small Batch Testing**: Send to verified email addresses only
3. **Monitor Metrics**: Check AWS CloudWatch for delivery statistics

### Step 3: Load Testing

```python
# Create test script for load testing
from django.core.management.base import BaseCommand
from birdsong.models import Contact
from emails.models import LSHNewsletter

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create test campaign
        campaign = LSHNewsletter.objects.create(
            name="Load Test Campaign",
            subject="Load Test",
            body=[{"type": "paragraph", "value": "Load testing content"}]
        )
        
        # Get subset of contacts for testing
        contacts = Contact.objects.all()[:100]  # Test with 100 contacts
        
        # Send campaign
        backend = SESEmailBackend()
        backend.send_campaign(None, campaign, contacts)
        
        self.stdout.write(f"Load test initiated for {len(contacts)} contacts")
```

## Phase 4: Monitoring and Analytics

### Step 1: CloudWatch Metrics

Monitor these key metrics:
- **Send**: Number of emails sent
- **Bounce**: Hard and soft bounces
- **Complaint**: Spam complaints
- **Delivery**: Successful deliveries
- **Reputation**: Sender reputation metrics

### Step 2: Custom Monitoring

Add monitoring to your application:

```python
# Add to birdsong SES backend
import boto3

def get_ses_statistics():
    """Get current SES sending statistics"""
    client = boto3.client('ses', region_name=settings.AWS_SES_REGION)
    
    # Get send quota
    quota = client.get_send_quota()
    
    # Get send statistics
    stats = client.get_send_statistics()
    
    return {
        'quota': quota,
        'statistics': stats['SendDataPoints'][-1] if stats['SendDataPoints'] else None
    }
```

### Step 3: Dashboard Integration

Consider integrating SES metrics into your admin dashboard:

```python
# Add to admin views
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def ses_dashboard(request):
    stats = get_ses_statistics()
    return render(request, 'admin/ses_dashboard.html', {'stats': stats})
```

## Phase 5: Migration Execution

### Step 1: Gradual Rollout

1. **Feature Flag Implementation**:
   ```python
   # Add to settings
   USE_SES_BACKEND = vars.vars.get("USE_SES_BACKEND", False)
   
   # Update backend selection
   if USE_SES_BACKEND:
       BIRDSONG_BACKEND_CLASS = "birdsong.backends.ses.SESEmailBackend"
   else:
       BIRDSONG_BACKEND_CLASS = "birdsong.backends.smtp.SMTPEmailBackend"
   ```

2. **A/B Testing**: Send to small groups first
3. **Monitor Closely**: Watch delivery rates and errors
4. **Gradual Increase**: Increase SES usage percentage

### Step 2: Full Migration

1. **Backup Current System**: Ensure SMTP fallback is available
2. **Switch to SES**: Set `USE_SES_BACKEND = True`
3. **Monitor for 24-48 hours**: Watch for any issues
4. **Remove SMTP Fallback**: After successful operation

## Rollback Procedures

### Emergency Rollback

If issues arise:

1. **Immediate**: Set `USE_SES_BACKEND = False`
2. **Restart Application**: Ensure settings take effect
3. **Monitor**: Verify SMTP backend is working
4. **Investigate**: Analyze SES logs and errors

### Troubleshooting Common Issues

1. **Rate Limiting**: Reduce `AWS_SES_RATE_LIMIT` setting
2. **Authentication Errors**: Verify AWS credentials
3. **Domain Issues**: Check domain verification status
4. **Bounce/Complaints**: Review email content and subscriber lists

## Best Practices

### Security
- Use IAM roles instead of access keys when possible
- Rotate access keys regularly
- Monitor AWS CloudTrail for API usage

### Performance
- Optimize batch sizes based on your sending patterns
- Use appropriate AWS region for your audience
- Monitor and adjust rate limits

### Compliance
- Implement proper unsubscribe handling
- Monitor bounce and complaint rates
- Maintain clean subscriber lists

## Cost Optimization

### SES Pricing (EU-West-1)
- **First 62,000 emails/month**: $0.10 per 1,000 emails
- **Additional emails**: $0.10 per 1,000 emails
- **Attachments**: $0.12 per GB

### Cost Comparison
- **Current SMTP**: Server maintenance + potential deliverability issues
- **AWS SES**: Predictable per-email pricing + improved deliverability

## Support and Resources

### AWS Documentation
- [SES Developer Guide](https://docs.aws.amazon.com/ses/)
- [SES API Reference](https://docs.aws.amazon.com/ses/latest/APIReference/)

### Monitoring Tools
- AWS CloudWatch
- SES Reputation Dashboard
- Third-party tools (SendGrid, Mailgun analytics)

### Emergency Contacts
- AWS Support (if you have a support plan)
- Internal team escalation procedures
