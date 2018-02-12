# Generated by Django 2.0.2 on 2018-02-12 12:47

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('user_id', models.IntegerField()),
                ('account_id', models.IntegerField()),
                ('documents', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
            ],
        ),
    ]