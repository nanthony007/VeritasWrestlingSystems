from django.db import models
from django_extensions.db.fields import AutoSlugField

"""Start of Folkstyle stuff, saved for potential later use...

class Team(models.Model):
    name = models.CharField(max_length=250, primary_key=True, unique=True)
    abbreviation = models.CharField(max_length=20)
    slug = models.SlugField(default=name)

    class Meta:
        verbose_name = 'FolkStyle Team'
        verbose_name_plural = 'FolkStyle Teams'

    def __str_(self):
        return self.name


class Wrestler(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    name = models.CharField(max_length=140, primary_key=True, unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_name')
    eligibility = models.CharField(
        max_length=5, blank=True,
        choices = YEAR_IN_SCHOOL_CHOICES, default=FRESHMAN)
    rating = models.IntegerField(default=1000)
    slug = AutoSlugField(('slug'), max_length=50, unique=True, populate_from=('name',))

    class Meta:
        verbose_name = 'FolkStyle Wrestler'
        verbose_name_plural = 'FolkStyle Wrestlers'

    def __str_(self):
        return self.name


class Matchdata(models.Model):
    matchID = models.CharField(max_length=140, primary_key=True, unique=True)
    date = models.DateField(null=True)
    focus = models.ForeignKey(Wrestler, on_delete=models.CASCADE, related_name='focus_wrestler', null=True)
    focus_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='focus_team_name', null=True)
    opponent = models.ForeignKey(Wrestler, on_delete=models.CASCADE, related_name='opp_wrestler', null=True)
    opp_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='opp_team_name', null=True)
    focus_score = models.IntegerField(null=True)
    opp_score = models.IntegerField(null=True)
    result = models.CharField(max_length=140, null=True)
    weight = models.IntegerField(null=True)
    mov = models.IntegerField(null=True)
    duration = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    hia = models.IntegerField(null=True)
    hic = models.IntegerField(null=True)
    hoa = models.IntegerField(null=True)
    hoc = models.IntegerField(null=True)
    da = models.IntegerField(null=True)
    dc = models.IntegerField(null=True)
    lsa = models.IntegerField(null=True)
    lsc = models.IntegerField(null=True)
    gba = models.IntegerField(null=True)
    gbc = models.IntegerField(null=True)
    ta = models.IntegerField(null=True)
    tc = models.IntegerField(null=True)
    su = models.IntegerField(null=True)
    e = models.IntegerField(null=True)
    r = models.IntegerField(null=True)
    cut = models.IntegerField(null=True)
    bd = models.IntegerField(null=True)
    mr = models.IntegerField(null=True)
    nf2 = models.IntegerField(null=True)
    nf4 = models.IntegerField(null=True)
    stalling = models.IntegerField(null=True)
    caution = models.IntegerField(null=True)
    tv = models.IntegerField(null=True)
    rt = models.IntegerField(null=True)
    opp_hia = models.IntegerField(null=True)
    opp_hic = models.IntegerField(null=True)
    opp_hoa = models.IntegerField(null=True)
    opp_hoc = models.IntegerField(null=True)
    opp_da = models.IntegerField(null=True)
    opp_dc = models.IntegerField(null=True)
    opp_lsa = models.IntegerField(null=True)
    opp_lsc = models.IntegerField(null=True)
    opp_gba = models.IntegerField(null=True)
    opp_gbc = models.IntegerField(null=True)
    opp_ta = models.IntegerField(null=True)
    opp_tc = models.IntegerField(null=True)
    opp_su = models.IntegerField(null=True)
    opp_e = models.IntegerField(null=True)
    opp_r = models.IntegerField(null=True)
    opp_cut = models.IntegerField(null=True)
    opp_bd = models.IntegerField(null=True)
    opp_mr = models.IntegerField(null=True)
    opp_nf2 = models.IntegerField(null=True)
    opp_nf4 = models.IntegerField(null=True)
    opp_stalling = models.IntegerField(null=True)
    opp_caution = models.IntegerField(null=True)
    opp_tv = models.IntegerField(null=True)
    opp_rt = models.IntegerField(null=True)
    hi_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ho_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    d_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ls_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    gb_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    t_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    td_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    npf = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    apm = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    vs = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_hi_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_ho_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_d_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_ls_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_gb_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_t_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_td_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_npf = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_apm = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_vs = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    class Meta:
        verbose_name = 'FolkStyle Match'
        verbose_name_plural = 'FolkStyle Matches'

    def __str_(self):
        return self.matchID


class Timeseries(models.Model):
    matchID = models.ForeignKey(Matchdata, on_delete=models.CASCADE, related_name='actions')
    event_num = models.IntegerField()
    event_lab = models.CharField(max_length=140)
    event_time = models.DecimalField(max_digits=10, decimal_places=2)
    blue = models.CharField(max_length=140)
    red = models.CharField(max_length=140)

    class Meta:
        verbose_name = 'FolkStyle TimeSeries'
        verbose_name_plural = 'FolkStyle TimeSeries'

    def __str_(self):
        return self.matchID


class Event(models.Model):
    name = models.CharField(max_length=140)
    matches = models.ManyToManyField(Matchdata, related_name='events')
    date = models.DateField(null=True)
    result = models.CharField(max_length=140, null=True)
    slug = models.SlugField(default=name)

    class Meta:
        verbose_name = 'FolStyle Event'
        verbose_name_plural = 'FolkStyle Events'

    def __str_(self):
        return self.name
"""


class FS_Team(models.Model):
    name = models.CharField(max_length=250, primary_key=True, unique=True)
    abbreviation = models.CharField(max_length=20)
    slug = AutoSlugField(('slug'), max_length=50, unique=True,
        populate_from=('abbreviation',))

    class Meta:
        verbose_name = 'FreeStyle Team'
        verbose_name_plural = 'FreeStyle Teams'

    def __str_(self):
        return self.abbreviation


class FS_Wrestler(models.Model):
    LEVELS = [
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Bronze', 'Bronze'),

    ]
    name = models.CharField(max_length=140, primary_key=True)
    team = models.ForeignKey(FS_Team, on_delete=models.CASCADE,
        default='Finger Lakes Wrestling Club/Titan Mercury Wrestling Club',
        related_name='team_name2')
    rating = models.IntegerField(default=1000)
    #level = models.CharField(choices=LEVELS, default=)
    slug = AutoSlugField(('slug'), max_length=50, unique=True, populate_from=('name',))

    class Meta:
        verbose_name = 'FreeStyle Wrestler'
        verbose_name_plural = 'FreeStyle Wrestlers'


class FS_Match(models.Model):
    matchID = models.CharField(max_length=140, primary_key=True, unique=True)
    date = models.DateField(null=True)
    focus = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE, related_name='focus_wrestler2', null=True)
    focus_team = models.ForeignKey(FS_Team, on_delete=models.CASCADE, related_name='focus_team_name2', null=True)
    opponent = models.ForeignKey(FS_Wrestler, on_delete=models.CASCADE, related_name='opp_wrestler2', null=True)
    opp_team = models.ForeignKey(FS_Team, on_delete=models.CASCADE, related_name='opp_team_name2', null=True)
    focus_score = models.IntegerField(null=True)
    opp_score = models.IntegerField(null=True)
    result = models.CharField(max_length=140, null=True)
    weight = models.IntegerField(null=True)
    mov = models.IntegerField(null=True)
    duration = models.CharField(max_length=140, null=True)
    # focus
    hia = models.IntegerField(null=True)
    hic2 = models.IntegerField(null=True)
    hic4 = models.IntegerField(null=True)
    hoa = models.IntegerField(null=True)
    hoc2 = models.IntegerField(null=True)
    hoc4 = models.IntegerField(null=True)
    da = models.IntegerField(null=True)
    dc2 = models.IntegerField(null=True)
    dc4 = models.IntegerField(null=True)
    lsa = models.IntegerField(null=True)
    lsc2 = models.IntegerField(null=True)
    lsc4 = models.IntegerField(null=True)
    gba = models.IntegerField(null=True)
    gbc2 = models.IntegerField(null=True)
    ta = models.IntegerField(null=True)
    tc2 = models.IntegerField(null=True)
    tc4 = models.IntegerField(null=True)
    exposure = models.IntegerField(null=True)
    gut = models.IntegerField(null=True)
    leg_lace = models.IntegerField(null=True)
    turn = models.IntegerField(null=True)
    recovery = models.IntegerField(null=True)
    pushout = models.IntegerField(null=True)
    passive = models.IntegerField(null=True)
    violation = models.IntegerField(null=True)
    # opponent
    opp_hia = models.IntegerField(null=True)
    opp_hic2 = models.IntegerField(null=True)
    opp_hic4 = models.IntegerField(null=True)
    opp_hoa = models.IntegerField(null=True)
    opp_hoc2 = models.IntegerField(null=True)
    opp_hoc4 = models.IntegerField(null=True)
    opp_da = models.IntegerField(null=True)
    opp_dc2 = models.IntegerField(null=True)
    opp_dc4 = models.IntegerField(null=True)
    opp_lsa = models.IntegerField(null=True)
    opp_lsc2 = models.IntegerField(null=True)
    opp_lsc4 = models.IntegerField(null=True)
    opp_gba = models.IntegerField(null=True)
    opp_gbc2 = models.IntegerField(null=True)
    opp_gbc4 = models.IntegerField(null=True)
    opp_ta = models.IntegerField(null=True)
    opp_tc2 = models.IntegerField(null=True)
    opp_tc4 = models.IntegerField(null=True)
    opp_exposure = models.IntegerField(null=True)
    opp_gut = models.IntegerField(null=True)
    opp_leg_lace = models.IntegerField(null=True)
    opp_turn = models.IntegerField(null=True)
    opp_recovery = models.IntegerField(null=True)
    opp_pushout = models.IntegerField(null=True)
    opp_passive = models.IntegerField(null=True)
    opp_violation = models.IntegerField(null=True)
    # calculated fields
    hi_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ho_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    d_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ls_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    gb_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    t_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    npf = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    apm = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    vs = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_hi_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_ho_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_d_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_ls_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_gb_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_t_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_npf = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_apm = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opp_vs = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    class Meta:
        verbose_name = 'FreeStyle Match'
        verbose_name_plural = 'FreeStyle Matches'

    def __str_(self):
        return self.matchID


class FS_TS(models.Model):
    matchID = models.ForeignKey(FS_Match, on_delete=models.CASCADE, related_name='actions2')
    event_num = models.IntegerField()
    event_lab = models.CharField(max_length=140)
    event_time = models.CharField(max_length=140)
    blue = models.CharField(max_length=140)
    red = models.CharField(max_length=140)

    class Meta:
        verbose_name = 'FreeStyle TimeSeries'
        verbose_name_plural = 'FreeStyle TimeSeries'

    def __str_(self):
        return self.matchID


class FS_Event(models.Model):
    name = models.CharField(max_length=140)
    matches = models.ManyToManyField(FS_Match, related_name='events2')
    date = models.DateField(null=True)
    slug = AutoSlugField(('slug'), max_length=50, unique=True, populate_from=('name',))

    class Meta:
        verbose_name = 'FreeStyle Event'
        verbose_name_plural = 'FreeStyle Events'

    def __str_(self):
        return self.name
