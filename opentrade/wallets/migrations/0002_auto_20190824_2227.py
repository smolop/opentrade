# Generated by Django 2.2.4 on 2019-08-24 22:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='ident',
            field=models.UUIDField(default=uuid.UUID('24bf5044-6fc2-4b26-bdde-524bb000cb58'), editable=False, primary_key=True, serialize=False),
        ),
    ]
