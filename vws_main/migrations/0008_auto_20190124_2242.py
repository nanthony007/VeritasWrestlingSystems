# Generated by Django 2.1.5 on 2019-01-25 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vws_main', '0007_auto_20190120_1920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_apm',
            new_name='apm',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_bd',
            new_name='bd',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_caution',
            new_name='caution',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_cut',
            new_name='cut',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_d_rate',
            new_name='d_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_da',
            new_name='da',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_dc',
            new_name='dc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_e',
            new_name='e',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_e_rate',
            new_name='e_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_score',
            new_name='focus_score',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_gb_rate',
            new_name='gb_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_gba',
            new_name='gba',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_gbc',
            new_name='gbc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_hi_rate',
            new_name='hi_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_hia',
            new_name='hia',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_hic',
            new_name='hic',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_ho_rate',
            new_name='ho_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_hoa',
            new_name='hoa',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_hoc',
            new_name='hoc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_ls_rate',
            new_name='ls_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_lsa',
            new_name='lsa',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_lsc',
            new_name='lsc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_mr',
            new_name='mr',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_nf2',
            new_name='nf2',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_nf4',
            new_name='nf4',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_apm',
            new_name='opp_apm',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_bd',
            new_name='opp_bd',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_caution',
            new_name='opp_caution',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_cut',
            new_name='opp_cut',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_d_rate',
            new_name='opp_d_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_da',
            new_name='opp_da',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_dc',
            new_name='opp_dc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_e',
            new_name='opp_e',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_e_rate',
            new_name='opp_e_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_gb_rate',
            new_name='opp_gb_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_gba',
            new_name='opp_gba',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_gbc',
            new_name='opp_gbc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_hi_rate',
            new_name='opp_hi_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_hia',
            new_name='opp_hia',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_hic',
            new_name='opp_hic',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_ho_rate',
            new_name='opp_ho_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_hoa',
            new_name='opp_hoa',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_hoc',
            new_name='opp_hoc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_ls_rate',
            new_name='opp_ls_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_lsa',
            new_name='opp_lsa',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_lsc',
            new_name='opp_lsc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_mr',
            new_name='opp_mr',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_nf2',
            new_name='opp_nf2',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_nf4',
            new_name='opp_nf4',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_r',
            new_name='opp_r',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_ride_rate',
            new_name='opp_ride_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_rt',
            new_name='opp_rt',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_score',
            new_name='opp_score',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_su',
            new_name='opp_su',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_t_rate',
            new_name='opp_t_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_ta',
            new_name='opp_ta',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_tc',
            new_name='opp_tc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_td_rate',
            new_name='opp_td_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_tv',
            new_name='opp_tv',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='red_vs',
            new_name='opp_vs',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_r',
            new_name='r',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_ride_rate',
            new_name='ride_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_rt',
            new_name='rt',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_su',
            new_name='su',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_t_rate',
            new_name='t_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_ta',
            new_name='ta',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_tc',
            new_name='tc',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_td_rate',
            new_name='td_rate',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_tv',
            new_name='tv',
        ),
        migrations.RenameField(
            model_name='matchdata',
            old_name='blue_vs',
            new_name='vs',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='blue',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='blue_team',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='red',
        ),
        migrations.RemoveField(
            model_name='matchdata',
            name='red_team',
        ),
        migrations.AddField(
            model_name='matchdata',
            name='focus',
            field=models.ForeignKey(default='Nick Lee', on_delete=django.db.models.deletion.CASCADE, related_name='focus_wrestler', to='vws_main.Wrestler'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='matchdata',
            name='focus_team',
            field=models.ForeignKey(default='Brown University', on_delete=django.db.models.deletion.CASCADE, related_name='focus_team_name', to='vws_main.Team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='matchdata',
            name='opp_team',
            field=models.ForeignKey(default='Brown University', on_delete=django.db.models.deletion.CASCADE, related_name='opp_team_name', to='vws_main.Team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='matchdata',
            name='opponent',
            field=models.ForeignKey(default='Nick Lee', on_delete=django.db.models.deletion.CASCADE, related_name='opp_wrestler', to='vws_main.Wrestler'),
            preserve_default=False,
        ),
    ]
