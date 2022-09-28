vars = {
    "DEBUG": True,
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
                'NAME': 'django_tests',
            },
        },
    },
    "LOGGING": {
        "filename": "../log/development.log",
        "level": "DEBUG",
    }
}
