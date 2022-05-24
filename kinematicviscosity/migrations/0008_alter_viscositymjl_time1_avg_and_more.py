# Generated by Django 4.0.4 on 2022-05-20 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kinematicviscosity', '0007_remove_viscositymjl_plustimemin11_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viscositymjl',
            name='time1_avg',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=3, verbose_name='Время истечения среднее 1, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='time2_avg',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=3, verbose_name='Время истечения среднее 2, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK1T1_sec',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=3, verbose_name='Время истечения K1T1, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK1T2_sec',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=3, verbose_name='Время истечения K1T2, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK2T1_sec',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=3, verbose_name='Время истечения K2T1, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='timeK2T2_sec',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=3, verbose_name='Время истечения K2T2, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='viscosity1',
            field=models.DecimalField(decimal_places=7, default='0', max_digits=11, verbose_name='Вязкость кинематическая 1'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='viscosity2',
            field=models.DecimalField(decimal_places=7, default='0', max_digits=11, verbose_name='Вязкость кинематическая 2'),
        ),
    ]