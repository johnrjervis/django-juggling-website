# Generated by Django 3.2 on 2022-01-05 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vlog', '0004_videocomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocomment',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
