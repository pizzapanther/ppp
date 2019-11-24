from django.urls import path

from polls.views import *

urlpatterns = [
  path('embed/<slug:slug>/<int:pid>/start', start_poll),
  path('embed/<slug:slug>/<int:pid>/end', end_poll),
  path('embed/<slug:slug>/<int:pid>/', embed),
  path('<slug:slug>/vote', vote),
  path('<slug:slug>/', presentation),
]
