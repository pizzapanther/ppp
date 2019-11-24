SOCIAL_AUTH_POSTGRES_JSONFIELD = True

AUTHENTICATION_BACKENDS = (
  #'social_core.backends.twitter.TwitterOAuth',

  'django.contrib.auth.backends.ModelBackend',
)
