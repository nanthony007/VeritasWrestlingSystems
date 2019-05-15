import django_filters
from django.forms.widgets import TextInput
from vws_main.models import FS_Wrestler, FS_Team, FS_Event

TIERS = (
    ('Grandmaster', 'Grandmaster (2500+)'),
    ('Master', 'Master (2300-2499)'),
    ('Expert', 'Expert (2000-2299)'),
    ('Class A', 'Class A (1800-1999)'),
    ('Class B', 'Class B (1600-1799)'),
    ('Class C', 'Class C (1400-1599)'),
    ('Class D', 'Class D (1200-1399)'),
    ('Class E', 'Class E (1000-1199)'),
    ('Amateur', 'Amateur (700-999)'),
    ('Novice', 'Novice (0-699)'),
)

FOLK_WEIGHTCLASSES = (
    (125, 125),
    (133, 133),
    (141, 141),
    (149, 149),
    (157, 157),
    (165, 165),
    (174, 174),
    (184, 184),
    (197, 197),
    (285, 285),
)

FREE_WEIGHTCLASSES = (
    (57, 57),
    (61, 61),
    (65, 65),
    (70, 70),
    (74, 74),
    (79, 79),
    (86, 86),
    (92, 92),
    (97, 97),
    (125, 125),
)


class FS_RatingsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Name",
        widget=TextInput(attrs={'placeholder': 'Name...'}))
    club = django_filters.ModelChoiceFilter(queryset=FS_Team.objects.values_list('abbreviation', flat=True),
        label='Club')
    weight = django_filters.ChoiceFilter(choices=FREE_WEIGHTCLASSES, label='Weight (kgs)')
    tier = django_filters.ChoiceFilter(choices=TIERS, label='Tier')

    class Meta:
        model = FS_Wrestler
        fields = ['name', 'club', 'tier', 'weight']


class FS_EventsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = FS_Event
        fields = ['name', 'date']
