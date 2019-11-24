from django.conf import settings

from huey.contrib.djhuey import task
import pusher

from polls.models import Poll

@task()
def push_stats(pres_slug, poll_id):
  poll = Poll.objects.get(id=poll_id)
  if poll.live:
    print('Sending Stats', poll.id, poll.question)
    pusher_client = pusher.Pusher(**settings.PUSHER)
    pusher_client.trigger(pres_slug, 'stats', poll.json_data())

    push_stats.schedule((pres_slug, poll_id), delay=2)
