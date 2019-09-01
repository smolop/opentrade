# Generated by Django 2.2.4 on 2019-08-25 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0005_auto_20190825_0821'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlannedSharesOperations',
            fields=[
                ('ref', models.AutoField(primary_key=True, serialize=False)),
                ('symbol', models.CharField(max_length=4)),
                ('date', models.DateField(auto_now=True)),
                ('timestamp', models.TimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('day', models.DateField()),
                ('time', models.DateTimeField()),
                ('max_price', models.FloatField()),
                ('min_price', models.FloatField()),
                ('operation', models.CharField(choices=[('b', 'buy'), ('s', 'sell')], max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'planned_shares_operation',
                'verbose_name_plural': 'planned_shares_operations',
                'ordering': ['-user', '-symbol', 'day', 'time', 'date', 'timestamp'],
            },
        ),
    ]
