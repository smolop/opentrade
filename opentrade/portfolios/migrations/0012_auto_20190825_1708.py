# Generated by Django 2.2.4 on 2019-08-25 17:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0011_auto_20190825_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='ident',
            field=models.UUIDField(default=uuid.UUID('967b6ee8-f0e4-47ea-9333-04bf51a52af8'), editable=False, primary_key=True, serialize=False),
        ),
    ]
