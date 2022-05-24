# Generated by Django 4.0.4 on 2022-05-20 14:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('viscosimeters', '0050_alter_viscosimeters_datecal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viscosimeters',
            name='dateCal',
            field=models.DateField(default=datetime.datetime(2022, 5, 20, 14, 37, 17, 907970, tzinfo=utc), verbose_name='Дата калибровки'),
        ),
        migrations.AlterField(
            model_name='viscosimeters',
            name='datePov',
            field=models.DateField(default=datetime.datetime(2022, 5, 20, 14, 37, 17, 907970, tzinfo=utc), verbose_name='Дата поверки'),
        ),
        migrations.AlterField(
            model_name='viscosimeters',
            name='datePovDedlain',
            field=models.DateField(default=datetime.datetime(2022, 5, 20, 17, 37, 17, 907970), verbose_name='Дата окончания поверки'),
        ),
    ]