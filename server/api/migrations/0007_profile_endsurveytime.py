# Generated by Django 3.0.8 on 2021-07-14 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210713_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='endsurveytime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]