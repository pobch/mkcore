# Generated by Django 2.0.2 on 2018-02-26 11:55

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('guest_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name="this is your room's name")),
                ('description', models.TextField()),
                ('room_login', models.CharField(max_length=200, unique=True)),
                ('room_password', models.CharField(max_length=100)),
                ('survey', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('guests', models.ManyToManyField(related_name='guest_in_rooms', to=settings.AUTH_USER_MODEL)),
                ('room_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='own_rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
