# Generated by Django 3.0.8 on 2021-08-24 15:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0020_memo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalSuggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggested_subcat', models.CharField(blank=True, max_length=255, null=True)),
                ('subcat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.InitSubCat')),
            ],
        ),
        migrations.CreateModel(
            name='SimScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similar', models.IntegerField(default=0)),
                ('not_similar', models.IntegerField(default=0)),
                ('is_valid', models.BooleanField(default=False)),
                ('doctype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.DocType')),
                ('first_sugg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_sugg', to='api.UserSuggestion')),
                ('second_sugg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_sugg', to='api.UserSuggestion')),
            ],
        ),
        migrations.CreateModel(
            name='GroupedAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boxes_id', models.TextField(null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('annot_type', models.CharField(max_length=500)),
                ('reason', models.TextField(blank=True, default='No reason', max_length=255, null=True)),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Document')),
                ('final_suggestion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.FinalSuggestion')),
                ('subcat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.InitSubCat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BoxAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annot_type', models.CharField(max_length=255)),
                ('suggested_subcat', models.CharField(blank=True, max_length=255, null=True)),
                ('box_id', models.IntegerField(default=999)),
                ('annotation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Annotation')),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.InitCat')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Document')),
                ('subcat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.InitSubCat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]