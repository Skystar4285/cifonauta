# Generated by Django 2.2.5 on 2019-09-14 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0038_auto_20190914_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sublocation',
            name='image_count',
        ),
        migrations.RemoveField(
            model_name='sublocation',
            name='video_count',
        ),
    ]