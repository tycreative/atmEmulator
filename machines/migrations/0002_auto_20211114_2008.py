# Generated by Django 3.2.8 on 2021-11-15 01:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='The current monetary balance of this ATM.', max_digits=19, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(1000000000)], verbose_name='Balance'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='minimum',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='The minimum balance allowed on this ATM.', max_digits=19, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(1000000000)], verbose_name='Minimum Balance'),
        ),
    ]
