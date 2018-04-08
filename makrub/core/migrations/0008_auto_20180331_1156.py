# Generated by Django 2.0.3 on 2018-03-31 11:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20180314_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='guests',
            field=models.ManyToManyField(related_name='rooms_guest', to=settings.AUTH_USER_MODEL),
        ),
    ]