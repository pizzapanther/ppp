from django import http
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

import pusher

from polls.models import Presentation, Poll


def presentation(request, slug):
  pres = get_object_or_404(Presentation, slug=slug)
  return TemplateResponse(request, 'presentation.html', {'pres': pres})


@staff_member_required
def embed(request, slug, pid):
  pres = get_object_or_404(Presentation, slug=slug)
  poll = get_object_or_404(Poll, id=pid, presentation__slug=slug)
  return TemplateResponse(request, 'embed.html', {'pres': pres, 'poll': poll})


@csrf_exempt
@staff_member_required
def start_poll(request, slug, pid):
  pres = get_object_or_404(Presentation, slug=slug)
  poll = get_object_or_404(Poll, id=pid, presentation__slug=slug)

  pres.poll_set.exclude(id=pid).update(live=False)
  poll.live = True
  poll.save()

  pusher_client = pusher.Pusher(**settings.PUSHER)
  pusher_client.trigger(pres.slug, 'go-live', poll.json_data())

  return http.JsonResponse({'status': 'started'})

@csrf_exempt
@staff_member_required
def end_poll(request, slug, pid):
  pres = get_object_or_404(Presentation, slug=slug)
  poll = get_object_or_404(Poll, id=pid, presentation__slug=slug)
  poll.live = False
  poll.save()

  pusher_client = pusher.Pusher(**settings.PUSHER)
  pusher_client.trigger(pres.slug, 'end-poll', {'poll': pid})

  return http.JsonResponse({'status': 'ended'})
