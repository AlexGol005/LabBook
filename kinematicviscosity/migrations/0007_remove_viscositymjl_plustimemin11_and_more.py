# Generated by Django 4.0.4 on 2022-05-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kinematicviscosity', '0006_remove_viscositymjl_accmeasurement_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viscositymjl',
            name='plustimemin11',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='plustimemin12',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='plustimemin21',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='plustimemin22',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='plustimesek11',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='plustimesek12',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='plustimesek21',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='plustimesek22',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='time11_sec',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='time12_sec',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='time21_sec',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='time22_sec',
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='plustimeminK1T1',
            field=models.DecimalField(decimal_places=0, default='0', max_digits=3, verbose_name='Время истечения K1T1, + мин'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='plustimeminK1T2',
            field=models.DecimalField(decimal_places=0, default='0', max_digits=3, verbose_name='Время истечения K1T2, + мин'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='plustimeminK2T1',
            field=models.DecimalField(decimal_places=0, default='0', max_digits=3, verbose_name='Время истечения K2T1, + мин'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='plustimeminK2T2',
            field=models.DecimalField(decimal_places=0, default='0', max_digits=3, verbose_name='Время истечения K2T2, + мин'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='plustimesekK1T1',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=5, verbose_name='Время истечения K1T1, + cек'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='plustimesekK1T2',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=5, verbose_name='Время истечения K1T2, + cек'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='plustimesekK2T1',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=5, verbose_name='Время истечения K2T1, + cек'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='plustimesekK2T2',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=5, verbose_name='Время истечения K2T2, + cек'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='timeK1T1_sec',
            field=models.DecimalField(decimal_places=4, default='0', max_digits=10, verbose_name='Время истечения K1T1, в секундах'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='timeK1T2_sec',
            field=models.DecimalField(decimal_places=4, default='0', max_digits=10, verbose_name='Время истечения K1T2, в секундах'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='timeK2T1_sec',
            field=models.DecimalField(decimal_places=4, default='0', max_digits=10, verbose_name='Время истечения K2T1, в секундах'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='timeK2T2_sec',
            field=models.DecimalField(decimal_places=4, default='0', max_digits=10, verbose_name='Время истечения K2T2, в секундах'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='Konstant1',
            field=models.DecimalField(decimal_places=6, default='0', max_digits=7, verbose_name='Константа вискозиметра № 1'),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='Konstant2',
            field=models.DecimalField(decimal_places=6, default='0', max_digits=7, verbose_name='Константа вискозиметра № 2'),
        ),
    ]
