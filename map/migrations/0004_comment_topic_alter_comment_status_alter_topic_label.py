# Generated by Django 4.1.3 on 2022-11-06 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_remove_topic_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.topic'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(default='approved', max_length=255),
        ),
        migrations.AlterField(
            model_name='topic',
            name='label',
            field=models.CharField(choices=[('Education', 'Education'), ('Environment', 'Environment'), ('World-Hunger', 'World-Hunger'), ('Democracy', 'Democracy'), ('Public-Health', 'Public-Health')], default='Education', max_length=255),
        ),
    ]
