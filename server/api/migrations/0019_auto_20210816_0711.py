# Generated by Django 3.0.8 on 2021-08-16 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20210816_0352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='endsurveytime',
            new_name='annot_endtime',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='instr_read',
            new_name='annotation_done',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='endtime',
            new_name='practice_endtime',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='starttime',
            new_name='practice_starttime',
        ),
        migrations.AddField(
            model_name='profile',
            name='consent_agreed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='instr_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='practice_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='review_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='review_endtime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='survey_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='survey_endtime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]