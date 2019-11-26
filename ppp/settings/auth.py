import os

SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GITHUB_KEY = os.environ.get('GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('GITHUB_SECRET')

SOCIAL_AUTH_TWITTER_KEY = os.environ.get('TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('TWITTER_SECRET')

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET')

SOCIAL_AUTH_REDDIT_KEY = os.environ.get('REDDIT_KEY')
SOCIAL_AUTH_REDDIT_SECRET = os.environ.get('REDDIT_SECRET')

AUTHENTICATION_BACKENDS = (
  'social_core.backends.facebook.FacebookOAuth2',
  'social_core.backends.twitter.TwitterOAuth',
  'social_core.backends.github.GithubOAuth2',
  'social_core.backends.reddit.RedditOAuth2',

  'django.contrib.auth.backends.ModelBackend',
)
