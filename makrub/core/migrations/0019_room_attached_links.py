# Generated by Django 2.0.6 on 2018-06-25 16:03

import core.models
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20180623_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='attached_links',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list),
        ),
    ]