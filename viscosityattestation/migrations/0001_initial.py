# Generated by Django 4.0.4 on 2022-05-16 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ViscosityMJL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('name', models.CharField(default='0', max_length=100, verbose_name='Наименование')),
                ('lot', models.CharField(max_length=100, verbose_name='Партия')),
                ('ndocument', models.CharField(choices=[('ГОСТ 33', 'ГОСТ 33'), ('МИ-01', 'МИ-01'), ('оценка', 'оценка вязкости')], default='МИ-01', max_length=100, verbose_name='Метод испытаний')),
                ('temperature', models.DecimalField(decimal_places=2, default='0', max_digits=5, verbose_name='Температура, ℃')),
                ('termostatition', models.BooleanField(blank=True, verbose_name='Термостатировано не менее 20 минут')),
                ('temperatureCheck', models.BooleanField(blank=True, verbose_name='Температура контролируется внешним поверенным термометром')),
                ('termometer', models.CharField(default='0', max_length=10, verbose_name='Внутренний номер термометра')),
                ('ViscosimeterNumber1', models.CharField(default='0', max_length=10, verbose_name='Заводской номер вискозиметра № 1')),
                ('Konstant1', models.DecimalField(decimal_places=10, default='0', max_digits=20, verbose_name='Константа вискозиметра № 1')),
                ('ViscosimeterNumber2', models.CharField(default='0', max_length=10, verbose_name='Заводской номер вискозиметра № 2')),
                ('Konstant2', models.DecimalField(decimal_places=10, default='0', max_digits=20, verbose_name='Константа вискозиметра № 2')),
                ('plustimemin11', models.DecimalField(decimal_places=0, default='0', max_digits=6, verbose_name='Время истечения 11, + мин')),
                ('plustimesek11', models.DecimalField(decimal_places=2, default='0', max_digits=5, verbose_name='Время истечения 11, + cек')),
                ('plustimemin12', models.DecimalField(decimal_places=0, default='0', max_digits=6, verbose_name='Время истечения 12, + мин')),
                ('plustimesek12', models.DecimalField(decimal_places=2, default='0', max_digits=5, verbose_name='Время истечения 12, + cек')),
                ('plustimemin21', models.DecimalField(decimal_places=0, default='0', max_digits=6, verbose_name='Время истечения 21, + мин')),
                ('plustimesek21', models.DecimalField(decimal_places=2, default='0', max_digits=5, verbose_name='Время истечения 21, + cек')),
                ('plustimemin22', models.DecimalField(decimal_places=0, default='0', max_digits=6, verbose_name='Время истечения 22, + мин')),
                ('plustimesek22', models.DecimalField(decimal_places=2, default='2', max_digits=5, verbose_name='Время истечения 22, + cек')),
                ('kriteriy', models.CharField(default='0,2', max_length=4, verbose_name='Критерий приемлемости измерений')),
                ('time11_sec', models.DecimalField(decimal_places=2, default='0', max_digits=6, verbose_name='Время истечения 11, в секундах')),
                ('performer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Измерение кинематической вязкости',
                'verbose_name_plural': 'Измерения кинематической вязкости',
            },
        ),
    ]
