# Generated by Django 4.0.4 on 2022-05-20 13:01

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kinematicviscosity', '0019_viscositymjl_termostatition_words'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viscositymjl',
            name='accMeasurement',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=5, verbose_name='Оценка приемлемости измерений'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='kriteriy',
            field=models.DecimalField(decimal_places=1, default=Decimal('0'), max_digits=2, verbose_name='Критерий приемлемости измерений'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='plustimeminK1T1',
            field=models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=3, verbose_name='Время истечения K1T1, + мин'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='plustimeminK1T2',
            field=models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=3, verbose_name='Время истечения K1T2, + мин'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='plustimeminK2T1',
            field=models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=3, verbose_name='Время истечения K2T1, + мин'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='plustimeminK2T2',
            field=models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=3, verbose_name='Время истечения K2T2, + мин'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='plustimesekK1T1',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=5, verbose_name='Время истечения K1T1, + cек'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='plustimesekK1T2',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=5, verbose_name='Время истечения K1T2, + cек'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='plustimesekK2T1',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=5, verbose_name='Время истечения K2T1, + cек'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='plustimesekK2T2',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=5, verbose_name='Время истечения K2T2, + cек'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK1T1_sec',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=7, verbose_name='Время истечения K1T1, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK1T2_sec',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=7, verbose_name='Время истечения K1T2, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK1_avg',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=7, verbose_name='Время истечения среднее 1, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK2T1_sec',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=7, verbose_name='Время истечения K2T1, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK2T2_sec',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=7, verbose_name='Время истечения K2T2, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK2_avg',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=7, verbose_name='Время истечения среднее 2, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='viscosity1',
            field=models.DecimalField(decimal_places=7, default=Decimal('0'), max_digits=20, verbose_name='Вязкость кинематическая 1'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='viscosity2',
            field=models.DecimalField(decimal_places=7, default=Decimal('0'), max_digits=20, verbose_name='Вязкость кинематическая 2'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='viscosityAVG',
            field=models.DecimalField(decimal_places=7, default=Decimal('0'), max_digits=20, verbose_name='Вязкость кинематическая среднее'),
        ),
    ]
