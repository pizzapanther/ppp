from django import forms
from django.contrib import admin
from django.contrib.postgres.forms import SplitArrayField

from polls.models import Poll, Vote

class VoteInline(admin.TabularInline):
  model = Vote
  raw_id_fields = ('user',)


class PollForm(forms.ModelForm):
  choices = SplitArrayField(
    forms.CharField(required=False, max_length=254), 8, remove_trailing_nulls=True)

  class Meta:
    model = Poll
    fields = '__all__'

  class Media:
    css = {'screen': ("admin/poll.css",)}


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
  list_display = ('question', 'slug', 'published', 'ended')
  raw_id_fields = ('next_poll',)
  inlines = [VoteInline]
  form = PollForm
