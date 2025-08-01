vars = {
    "SITE_URL": "http://localhost:8000",
    "DEBUG": True,
    "ADMINS": [],
    "SERVER_EMAIL": "system@localhost",
    "DEFAULT_FROM_EMAIL": "webmaster@localhost",
    "BIRDSONG_FROM_EMAIL": "newsletter@localhost",
    "SECRET_KEY": 'eo3taeleev0ZeiReeteer9Xeepoor3quai7poorai1laishaeshohmaej6weiC3e',
    "ALLOWED_HOSTS": [
        'localhost',
        '127.0.0.1',
    ],
    "DATABASES": {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'strafrecht',
            'USER': 'django',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5434',
            'TEST': {
                'NAME': 'strafrecht_test',
            },
        },
    },
    "LOGGING": {
        "filename": "../log/development.log",
        "level": "DEBUG",
    },
    "DEV_APPS": [
    	"django_extensions",
    ],

    # AWS SES Configuration (required for all email sending)
    "AWS_ACCESS_KEY_ID": "your-aws-access-key-id",
    "AWS_SECRET_ACCESS_KEY": "your-aws-secret-access-key",
    "AWS_SES_REGION": "eu-central-1",  # Choose appropriate region for your audience
    "AWS_SES_BATCH_SIZE": 10,       # Number of emails per batch
    "AWS_SES_RATE_LIMIT": 14,       # Emails per second (adjust based on your SES limits)

    # Newsletter Backend Configuration
    "USE_SES_BACKEND": True,  # Set to False to use SMTP fallback
    "BIRDSONG_BACKEND_CLASS": "birdsong.backends.ses.SESEmailBackend",
    "BIRDSONG_FALLBACK_BACKEND": "birdsong.backends.smtp.SMTPEmailBackend",

    # SES Monitoring and Analytics
    "SES_ENABLE_CLOUDWATCH": True,
    "SES_BOUNCE_TOPIC_ARN": "arn:aws:sns:eu-central-1:your-account:ses-bounces-strafrecht",
    "SES_COMPLAINT_TOPIC_ARN": "arn:aws:sns:eu-central-1:your-account:ses-complaints-strafrecht",
}
