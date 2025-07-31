# AWS SES Configuration Template
# Copy this to your actual vars.py and update with your AWS credentials

vars = {
    "SITE_URL": "https://strafrecht-online.org",
    "DEBUG": False,
    "ADMINS": [
        ('Admin', 'admin@strafrecht-online.org'),
    ],
    "SERVER_EMAIL": "system@strafrecht-online.org",
    "DEFAULT_FROM_EMAIL": "webmaster@strafrecht-online.org",
    "BIRDSONG_FROM_EMAIL": "newsletter@strafrecht-online.org",
    "SECRET_KEY": 'your-secret-key-here',
    "ALLOWED_HOSTS": [
        'strafrecht-online.org',
        'www.strafrecht-online.org',
    ],
    "DATABASES": {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'strafrecht',
            'USER': 'django',
            'PASSWORD': 'your-db-password',
            'HOST': 'localhost',
            'PORT': '5434',
            'TEST': {
                'NAME': 'strafrecht_test',
            },
        },
    },
    "LOGGING": {
        "filename": "../log/production.log",
        "level": "INFO",
    },
    "EMAIL": {
        "host": "localhost",
        "port": "25",
        "login": "",
        "password": "",
    },
    
    # AWS SES Configuration
    "AWS_ACCESS_KEY_ID": "your-aws-access-key-id",
    "AWS_SECRET_ACCESS_KEY": "your-aws-secret-access-key",
    "AWS_SES_REGION": "eu-west-1",  # Choose appropriate region for your audience
    "AWS_SES_BATCH_SIZE": 10,       # Number of emails per batch
    "AWS_SES_RATE_LIMIT": 14,       # Emails per second (adjust based on your SES limits)
    
    # Newsletter Backend Configuration
    "USE_SES_BACKEND": True,  # Set to False to use SMTP fallback
    "BIRDSONG_BACKEND_CLASS": "birdsong.backends.ses.SESEmailBackend",
    "BIRDSONG_FALLBACK_BACKEND": "birdsong.backends.smtp.SMTPEmailBackend",
    
    # SES Monitoring and Analytics
    "SES_ENABLE_CLOUDWATCH": True,
    "SES_BOUNCE_TOPIC_ARN": "arn:aws:sns:eu-west-1:your-account:ses-bounces-strafrecht",
    "SES_COMPLAINT_TOPIC_ARN": "arn:aws:sns:eu-west-1:your-account:ses-complaints-strafrecht",
    
    # Development overrides (when DEBUG=True)
    "DEV_APPS": [
        "django_extensions",
    ],
}

# Development-specific overrides
if vars.get("DEBUG", False):
    # Use local SMTP for development
    vars.update({
        "USE_SES_BACKEND": False,
        "BIRDSONG_BACKEND_CLASS": "birdsong.backends.smtp.SMTPEmailBackend",
        "EMAIL": {
            "host": "localhost",
            "port": "1025",  # mailcatcher port
            "login": "",
            "password": "",
        },
    })
