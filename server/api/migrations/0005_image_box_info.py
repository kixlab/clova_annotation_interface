# Generated by Django 3.0.8 on 2020-08-04 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_image_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='box_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
