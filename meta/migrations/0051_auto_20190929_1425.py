# Generated by Django 2.2.5 on 2019-09-29 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0050_media_size_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='size',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
