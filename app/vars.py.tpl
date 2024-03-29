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
    "EMAIL": {
    	"host": "server address",
    	"port": "25",
    	"login": "your@email.address",
    	"password": "password",
    },
}
