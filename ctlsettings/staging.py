import sys
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


def common(**kwargs):
    # required args
    project = kwargs['project']
    base = kwargs['base']
    STATIC_ROOT = kwargs['STATIC_ROOT']
    INSTALLED_APPS = kwargs['INSTALLED_APPS']

    # optional args
    s3static = kwargs.get('s3static', True)
    cloudfront = kwargs.get('cloudfront', None)
    s3prefix = kwargs.get('s3prefix', 'ctl')

    DEBUG = False
    STAGING_ENV = True
    ENVIRONMENT = 'staging'

    STATSD_PREFIX = project + "-staging"

    MEDIA_ROOT = '/var/www/' + project + '/uploads/'

    # put any static media here to override app served static media
    STATICMEDIA_MOUNTS = [
        ('/sitemedia', '/var/www/' + project + '/' + project + '/sitemedia'),
    ]

    if s3static:
        # serve static files off S3
        AWS_STORAGE_BUCKET_NAME = s3prefix + "-" + project + "-static-stage"
        AWS_S3_OBJECT_PARAMETERS = {
            'ACL': 'public-read',
        }
        DEFAULT_FILE_STORAGE = 'ctlsettings.storages.UploadsStorage'
        STATICFILES_STORAGE = 'ctlsettings.storages.MediaStorage'

        if cloudfront:
            AWS_S3_CUSTOM_DOMAIN = cloudfront + '.cloudfront.net'
            S3_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
            STATIC_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
        else:
            S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
            STATIC_URL = ('https://%s.s3.amazonaws.com/media/'
                          % AWS_STORAGE_BUCKET_NAME)

        MEDIA_URL = S3_URL + 'uploads/'
        AWS_QUERYSTRING_AUTH = False
    else:
        # non S3 mode
        STATICFILES_DIRS = ()
        STATIC_ROOT = "/var/www/" + project + "/" + project + "/media/"

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'timestamped': {
                'format': '{asctime} {levelname} {message}',
                'style': '{'
            },
        },
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'backupCount': 4,
                'maxBytes': 10*1024*1024,
                'filename': '/var/log/django/' + project + '.log',
                'formatter': 'timestamped',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }

    return locals()


def init_sentry(sentry_dsn: str) -> None:
    if sentry_dsn and \
        ('migrate' not in sys.argv) and \
            ('collectstatic' not in sys.argv):
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[DjangoIntegration()],
            debug=True,
            environment='staging',
            traces_sample_rate=1.0,
        )
