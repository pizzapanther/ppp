from django import http
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

import pusher

from polls.models import Presentation, Poll, Vote
from polls.tasks import push_stats

def presentation(request, slug):
  pres = get_object_or_404(Presentation, slug=slug)
  context = {'pres': pres, 'key': settings.PUSHER['key']}
  return TemplateResponse(request, 'presentation.html', context)


@staff_member_required
def embed(request, slug, pid):
  pres = get_object_or_404(Presentation, slug=slug)
  poll = get_object_or_404(Poll, id=pid, presentation__slug=slug)
  context = {'pres': pres, 'poll': poll, 'key': settings.PUSHER['key']}
  return TemplateResponse(request, 'embed.html', context)


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

  push_stats.schedule((pres.slug, poll.id), delay=2)

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


@csrf_exempt
@login_required
def vote(request, slug):
  pid = request.POST.get('poll')
  vote = int(request.POST.get('vote'))
  poll = get_object_or_404(Poll, id=pid, presentation__slug=slug)

  obj, created = Vote.objects.get_or_create(
    poll=poll,
    user=request.user,
    defaults={'choice': vote},
  )

  if not created:
    obj.choice = vote
    obj.save()

  return http.JsonResponse({'status': 'recorded'})
