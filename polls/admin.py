from django import forms
from django.contrib import admin
from django.contrib.postgres.forms import SplitArrayField

from polls.models import Presentation, Poll, Vote

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

class PollInline(admin.TabularInline):
  model = Poll

def reset_votes(modeladmin, request, queryset):
    ids = queryset.values_list('id', flat=True)
    Vote.objects.filter(poll__presentation__in=ids).delete()

reset_votes.short_description = "Reset Votes"

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug')
  inlines = [PollInline]
  actions = [reset_votes]

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
  list_display = ('question', 'presentation', 'live', 'total_votes')
  raw_id_fields = ('presentation',)
  inlines = [VoteInline]
  form = PollForm

  def total_votes(self, obj):
    if obj:
      return obj.vote_set.all().count()
