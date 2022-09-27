vars = {
    "DEBUG": True,
    "SECRET_KEY": '#g*o!3=v$8+ag9%^&llf6h-fhm9zsrjlmb+s0)g&#*b1*8l##w',
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
    }
}
