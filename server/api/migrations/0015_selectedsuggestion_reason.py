# Generated by Django 3.0.8 on 2021-08-04 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_remove_profile_consent_agreed'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedsuggestion',
            name='reason',
            field=models.TextField(blank=True, default='No reason', max_length=255, null=True),
        ),
    ]
