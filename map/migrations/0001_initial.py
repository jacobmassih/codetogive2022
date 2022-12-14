# Generated by Django 4.1.3 on 2022-11-06 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=20)),
                ('comment', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=20)),
                ('date', models.DateTimeField(auto_now=True)),
                ('city', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('likes', models.BigIntegerField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.comment')),
            ],
        ),
    ]
