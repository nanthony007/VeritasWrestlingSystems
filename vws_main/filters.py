from django.contrib.auth.models import User
import django_filters
from vws_main.models import Wrestler, Team, Matchdata
from django_filters import rest_framework as filters

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

WEIGHTCLASSES = (
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

class RatingsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    team = django_filters.ModelChoiceFilter(queryset=Team.objects.values_list('name', flat=True))
    tier = django_filters.ChoiceFilter(choices=TIERS, label='Tier')

    class Meta:
        model = Wrestler
        fields = ['name', 'team', 'tier',]


class WeightClassFilter(django_filters.FilterSet):
    weight_classes = django_filters.ChoiceFilter(choices=WEIGHTCLASSES, label='Weight Classes')

    class Meta:
        model = Matchdata
        fields = ['weight_classes',]
