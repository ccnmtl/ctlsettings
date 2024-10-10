from django.conf import settings


def env(request):
    """
    Environment variables from settings for use in templates.
    """
    return {
        'STAGING_ENV': getattr(settings, 'STAGING_ENV', False),
        'ENVIRONMENT': getattr(settings, 'ENVIRONMENT', 'development'),
        'SENTRY_KEY': getattr(settings, 'SENTRY_KEY', None),
    }
