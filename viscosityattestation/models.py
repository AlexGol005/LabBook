from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ViscosityMJL(models.Model):
    date = models.DateField('Дата', default=timezone.now)
    name = models.CharField('Наименование', max_length=100)
    lot = models.CharField('Партия', max_length=100)
    ndocumentoptional = (('ГОСТ 33', 'ГОСТ 33'),
                         ('МИ-01', 'МИ-01'),
                         ('оценка', 'оценка вязкости'))
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=ndocumentoptional, default='МИ-01')
    temperature = models.DecimalField('Температура, ℃', max_digits=5, decimal_places=2)
    termostatition = models.BooleanField(verbose_name='Термостатировано не менее 20 минут', blank=False)
    temperatureCheck = models.BooleanField(verbose_name='Температура контролируется внешним поверенным термометром', blank=False)
    termometer = models.CharField('Внутренний номер термометра', max_length=10)
    ViscosimeterNumber1 = models.CharField('Заводской номер вискозиметра № 1', max_length=10)
    Konstant1 = models.DecimalField('Константа вискозиметра № 1', max_digits=20, decimal_places=10, default='0')
    ViscosimeterNumber2 = models.CharField('Заводской номер вискозиметра № 2', max_length=10)
    Konstant2 = models.DecimalField('Константа вискозиметра № 2', max_digits=20, decimal_places=10, default='0')
    plustimemin11 = models.DecimalField('Время истечения 11, + мин', max_digits=6, decimal_places=0)
    plustimesek11 = models.DecimalField('Время истечения 11, + cек', max_digits=5, decimal_places=2)
    plustimemin12 = models.DecimalField('Время истечения 12, + мин', max_digits=6, decimal_places=0)
    plustimesek12 = models.DecimalField('Время истечения 12, + cек', max_digits=5, decimal_places=2)
    plustimemin21 = models.DecimalField('Время истечения 21, + мин', max_digits=6, decimal_places=0)
    plustimesek21 = models.DecimalField('Время истечения 21, + cек', max_digits=5, decimal_places=2)
    plustimemin22 = models.DecimalField('Время истечения 22, + мин', max_digits=6, decimal_places=0)
    plustimesek22 = models.DecimalField('Время истечения 22, + cек', max_digits=5, decimal_places=2)
    kriteriy = models.CharField('Критерий приемлемости измерений', max_length=4, default='0,2')
    performer = models.ForeignKey(User, verbose_name='Исполнитель', on_delete=models.PROTECT)
    time11_sec = models.DecimalField('Время истечения 11, в секундах', max_digits=6, decimal_places=2, default='0')
    time12_sec = models.DecimalField('Время истечения 11, в секундах', max_digits=6, decimal_places=2, default='0')
    time21_sec = models.DecimalField('Время истечения 11, в секундах', max_digits=6, decimal_places=2, default='0')
    time22_sec = models.DecimalField('Время истечения 11, в секундах', max_digits=6, decimal_places=2, default='0')
    time1_avg = models.DecimalField('Время истечения среднее 1, в секундах', max_digits=6, decimal_places=2, default='0')
    time2_avg = models.DecimalField('Время истечения среднее 2, в секундах', max_digits=6, decimal_places=2, default='0')
    viscosity1 = models.DecimalField('Вязкость кинематическая 1', max_digits=20, decimal_places=6, default='0')
    viscosity2 = models.DecimalField('Вязкость кинематическая 2', max_digits=20, decimal_places=6, default='0')



    def save(self, *args, **kwargs):
        # set the full name whenever the object is saved
        a = self.plustimemin11 * 60 + self.plustimesek11
        b = self.plustimemin12 * 60 + self.plustimesek12
        c = self.plustimemin21 * 60 + self.plustimesek21
        d = self.plustimemin22 * 60 + self.plustimesek22
        self.time11_sec = a
        self.time12_sec = b
        self.time21_sec = c
        self.time22_sec = d
        self.time1_avg = (a + c)/2
        self.time2_avg = (b + d)/2
        self.viscosity1 = self.Konstant1 * self.time1_avg
        self.viscosity2 = self.Konstant2 * self.time2_avg

        super(ViscosityMJL, self).save(*args, **kwargs)

    def __str__(self):
        return f' {self.name}  п.{self.lot};  {self.temperature} t ℃;   {self.date}'


    class Meta:
        verbose_name = 'Измерение кинематической вязкости'
        verbose_name_plural = 'Измерения кинематической вязкости'


