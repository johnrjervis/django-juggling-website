# Generated by Django 3.2 on 2021-05-08 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vlog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugglingvideo',
            name='filename',
            field=models.CharField(default='', max_length=60),
        ),
    ]
