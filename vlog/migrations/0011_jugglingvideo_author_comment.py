# Generated by Django 3.2 on 2022-02-01 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vlog', '0010_acknowledgement'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugglingvideo',
            name='author_comment',
            field=models.TextField(default=''),
        ),
    ]
