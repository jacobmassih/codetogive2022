# Generated by Django 4.1.3 on 2022-11-06 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_alter_topic_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='comment',
        ),
    ]