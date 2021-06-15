# Generated by Django 3.0.8 on 2021-06-14 10:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20210523_2302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='label',
        ),
        migrations.RemoveField(
            model_name='usercat',
            name='cat_no',
        ),
        migrations.RemoveField(
            model_name='usersubcat',
            name='subcat_no',
        ),
        migrations.AddField(
            model_name='annotation',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.UserCat'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='subcat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.UserSubcat'),
        ),
        migrations.AddField(
            model_name='usercat',
            name='made_at',
            field=models.IntegerField(default=9999, null=True),
        ),
        migrations.AddField(
            model_name='usersubcat',
            name='made_at',
            field=models.IntegerField(default=9999, null=True),
        ),
        migrations.CreateModel(
            name='DefAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boxes_id', models.TextField(null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('confidence', models.BooleanField(default=True, null=True)),
                ('is_alive', models.BooleanField(default=False)),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.UserCat')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Document')),
                ('subcat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.UserSubcat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
        ),
    ]