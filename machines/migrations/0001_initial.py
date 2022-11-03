# Generated by Django 3.2.8 on 2021-11-14 16:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(help_text='The address associated with this ATM.', max_length=150, verbose_name='ATM Location')),
                ('status', models.BooleanField(default=True, help_text='The current status of this ATM.', verbose_name='Active')),
                ('minimum', models.DecimalField(decimal_places=2, default=0.0, help_text='The minimum balance allowed on this ATM.', max_digits=19, verbose_name='Minimum Balance')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, help_text='The current monetary balance of this ATM.', max_digits=19, verbose_name='Balance')),
                ('maintenance', models.DateField(blank=True, help_text='The next date in which this ATM is to be maintenanced.', verbose_name='Maintenance Date')),
                ('last_refill', models.DateField(blank=True, default=django.utils.timezone.now, help_text='The last date in which this ATM was refilled.', verbose_name='Last Refill Date')),
                ('next_refill', models.DateField(blank=True, help_text='The next date in which this ATM is to be refilled.', verbose_name='Next Refill Date')),
                ('x', models.PositiveIntegerField(default=1, help_text="This ATM's x-axis position on the map.", validators=[django.core.validators.MaxValueValidator(1920)], verbose_name='X-Axis Position')),
                ('y', models.PositiveIntegerField(default=1, help_text="This ATM's y-axis position on the map.", validators=[django.core.validators.MaxValueValidator(960)], verbose_name='Y-Axis Position')),
            ],
        ),
        migrations.CreateModel(
            name='Refill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, help_text='The amount added to this machine.', max_digits=19, verbose_name='Refill Amount')),
                ('previous', models.DecimalField(decimal_places=2, help_text='The previous balance of this machine.', max_digits=19, verbose_name='Previous Balance')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, help_text='The date this machine was refilled.', verbose_name='Refill Date')),
                ('machine', models.ForeignKey(help_text='The machine that was refilled.', on_delete=django.db.models.deletion.DO_NOTHING, related_name='refill', to='machines.machine', verbose_name='Machine')),
            ],
        ),
    ]