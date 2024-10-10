from setuptools import setup

setup(
    name='ctlsettings',
    version='0.4.0',
    author='Columbia University Center for Teaching and Learning',
    author_email='ctl-dev@columbia.edu',
    url='https://github.com/ccnmtl/ctlsettings',
    description='Columbia CTL common Django base settings',
    long_description='common settings we use across all our projects',
    install_requires=[
        'django-cas-ng',
        'django-debug-toolbar',
        'coverage',
        'django-smoketest',
        'django-extensions',
        'django-statsd-mozilla',
        'sentry-sdk',
        'django-storages',
        'boto3',
        'requests',
        'statsd',
        'gunicorn',
        'django-impersonate',
    ],
    scripts=[],
    license='GPL-3.0-or-later',
    platforms=['any'],
    packages=['ctlsettings', 'ctlsettings.templates'],
    package_data={
        'ctlsettings': ['*.py'],
        'ctlsettings.templates': ['*/*.html'],
    },
)
