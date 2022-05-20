# Generated by Django 4.0.4 on 2022-05-20 08:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viscosimeters', '0006_alter_viscosimeters_datecal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viscosimeters',
            name='dateCal',
            field=models.DateField(default=datetime.datetime(2022, 5, 20, 11, 46, 54, 176503), verbose_name='Дата калибровки'),
        ),
        migrations.AlterField(
            model_name='viscosimeters',
            name='datePov',
            field=models.DateField(default=datetime.datetime(2022, 5, 20, 11, 46, 54, 176503), verbose_name='Дата поверки'),
        ),
        migrations.AlterField(
            model_name='viscosimeters',
            name='datePovDedlain',
            field=models.DateField(default=datetime.datetime(2022, 5, 20, 11, 46, 54, 176503), verbose_name='Дата окончания поверки'),
        ),
    ]
