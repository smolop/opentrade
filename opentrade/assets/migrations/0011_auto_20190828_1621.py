# Generated by Django 2.2.4 on 2019-08-28 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0010_scheduledsharesoperations_share_reference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduledsharesoperations',
            name='share_reference',
        ),
        migrations.AlterField(
            model_name='scheduledsharesoperations',
            name='operation',
            field=models.CharField(choices=[('b', 'buy'), ('s', 'sell')], max_length=1),
        ),
    ]
