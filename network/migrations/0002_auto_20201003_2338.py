# Generated by Django 3.0.8 on 2020-10-04 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes_num',
        ),
        migrations.RemoveField(
            model_name='user',
            name='followers_num',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following_num',
        ),
    ]
