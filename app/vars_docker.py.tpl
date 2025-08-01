import os
from urllib.parse import urlparse

# Parse DATABASE_URL if provided
database_url = os.environ.get('DATABASE_URL')
if database_url:
    url = urlparse(database_url)
    database_config = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port or 5432,
        'TEST': {
            'NAME': f"{url.path[1:]}_test",
        },
    }
else:
    database_config = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'strafrecht'),
        'USER': os.environ.get('POSTGRES_USER', 'django'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'TEST': {
            'NAME': f"{os.environ.get('POSTGRES_DB', 'strafrecht')}_test",
        },
    }

vars = {
    "SITE_URL": os.environ.get('SITE_URL', 'http://localhost:8000'),
    "DEBUG": os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes', 'on'),
    "ADMINS": [
        (admin.split(':')[0], admin.split(':')[1]) 
        for admin in os.environ.get('ADMINS', '').split(',') 
        if ':' in admin
    ],
    "SERVER_EMAIL": os.environ.get('SERVER_EMAIL', 'system@localhost'),
    "DEFAULT_FROM_EMAIL": os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
    "BIRDSONG_FROM_EMAIL": os.environ.get('BIRDSONG_FROM_EMAIL', 'newsletter@localhost'),
    "SECRET_KEY": os.environ.get('SECRET_KEY', 'change-me-in-production'),
    "ALLOWED_HOSTS": [
        host.strip() 
        for host in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
        if host.strip()
    ],
    "DATABASES": {
        'default': database_config,
    },
    "LOGGING": {
        "filename": "/app/log/application.log",
        "level": os.environ.get('LOG_LEVEL', 'INFO'),
    },
    "DEV_APPS": [
        app.strip() 
        for app in os.environ.get('DEV_APPS', '').split(',')
        if app.strip()
    ] if os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes', 'on') else [],

    # AWS SES Configuration
    "AWS_ACCESS_KEY_ID": os.environ.get('AWS_ACCESS_KEY_ID', ''),
    "AWS_SECRET_ACCESS_KEY": os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
    "AWS_SES_REGION": os.environ.get('AWS_SES_REGION', 'eu-central-1'),
    "AWS_SES_BATCH_SIZE": int(os.environ.get('AWS_SES_BATCH_SIZE', '10')),
    "AWS_SES_RATE_LIMIT": int(os.environ.get('AWS_SES_RATE_LIMIT', '14')),

    # Newsletter Backend Configuration
    "USE_SES_BACKEND": os.environ.get('USE_SES_BACKEND', 'True').lower() in ('true', '1', 'yes', 'on'),
    "BIRDSONG_BACKEND_CLASS": os.environ.get('BIRDSONG_BACKEND_CLASS', 'birdsong.backends.ses.SESEmailBackend'),
    "BIRDSONG_FALLBACK_BACKEND": os.environ.get('BIRDSONG_FALLBACK_BACKEND', 'birdsong.backends.smtp.SMTPEmailBackend'),

    # SES Monitoring and Analytics
    "SES_ENABLE_CLOUDWATCH": os.environ.get('SES_ENABLE_CLOUDWATCH', 'True').lower() in ('true', '1', 'yes', 'on'),
    "SES_BOUNCE_TOPIC_ARN": os.environ.get('SES_BOUNCE_TOPIC_ARN', ''),
    "SES_COMPLAINT_TOPIC_ARN": os.environ.get('SES_COMPLAINT_TOPIC_ARN', ''),

    # Redis Configuration
    "REDIS_URL": os.environ.get('REDIS_URL', 'redis://redis:6379/0'),
    "CELERY_BROKER_URL": os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0'),

    # Static and Media Files
    "STATIC_ROOT": "/app/staticfiles",
    "MEDIA_ROOT": "/app/media",
    "STATIC_URL": "/static/",
    "MEDIA_URL": "/media/",
}
