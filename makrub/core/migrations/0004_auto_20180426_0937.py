# Generated by Django 2.0.3 on 2018-04-26 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180424_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_password',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]