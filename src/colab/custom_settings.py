from settings import *

DEBUG = False

TEMPLATE_DEBUG = False

TIME_ZONE = 'America/Sao_Paulo'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
    ('pt-BR', gettext('Portuguese')),
)

INSTALLED_APPS = INSTALLED_APPS + (
    # Not standard apps
    'south',
    'cliauth',

    # Own apps
    'api',
    'super_archives',
    'rss',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SERVER_EMAIL = '"Colab Interlegis" <noreply@interlegis.leg.br>'
EMAIL_HOST_USER = SERVER_EMAIL

#SOLR_HOSTNAME = 'solr.interlegis.leg.br'
SOLR_HOSTNAME = '10.1.2.154'
SOLR_PORT = '8080'
SOLR_SELECT_PATH = '/solr/select'

SOLR_COLAB_URI = 'http://colab.interlegis.leg.br'
SOLR_BASE_QUERY = """
    ((Type:changeset OR Type:ticket OR Type:wiki OR Type:thread) AND Title:["" TO *])
"""

try:
    from settings_local import *
except ImportError:
    pass
