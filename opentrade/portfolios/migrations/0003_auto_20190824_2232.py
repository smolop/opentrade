# Generated by Django 2.2.4 on 2019-08-24 22:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0002_auto_20190824_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='ident',
            field=models.UUIDField(default=uuid.UUID('01619209-7f9e-4fa8-b892-cb6c34355dc9'), editable=False, primary_key=True, serialize=False),
        ),
    ]
