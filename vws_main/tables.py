import django_tables2 as tables
from django_tables2.utils import A
from vws_main.models import Wrestler, Event

class WrestlerTable(tables.Table):
    name = tables.LinkColumn('wrestler_detail_view', args=[A('slug')])
    team = tables.RelatedLinkColumn('team_roster', accessor='team.name', args=[A('team.slug')], verbose_name='Team')

    class Meta:
        model = Wrestler
        attrs = {'class' : 'table table-striped table-hover table-sm'}
        exclude = ['eligibility', 'competitions', 'slug']

class EventTable(tables.Table):
    name = tables.LinkColumn('events_detail_view', args=[A('slug')])

    class Meta:
        model = Event
        attrs = {'class' : 'table table-striped'}
        exclude = ['id', 'slug']
