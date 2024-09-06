from django.db import models
from PIL import Image
from django.db import models
from django.urls import reverse

SEASONS = [('теплое время года', 'теплое время года'),('лето','лето'), ('зима','зима'), ('весна','весна'), ('осень','осень')] 
class Hike(models.Model):
    how_long = models.IntegerField('Сколько дней',  blank=True, null=True, default='1')
    season = models.CharField('Сезон', max_length=10000, blank=True, choices=SEASONS, null=True, default='теплое время года')
    country = models.CharField('Страна', max_length=10000, blank=True, null=True, default='Россия')
    region = models.CharField('Регион', max_length=10000, blank=True, null=True, default='Северо-Запад')
    title = models.CharField('Заголовок', max_length=10000, blank=True, null=True)
    reality = models.BooleanField(verbose_name='Пройдено',
                                           blank=True, null=True, default=False)
    date = models.DateField('Дата добавления записи', auto_now_add=True, db_index=True)
    date_fact = models.DateField('Дата похода', blank=True, null=True)
    metatitle = models.CharField('Метазаголовок страницы', max_length=10000, blank=True, null=True)
    description = models.TextField('Метаописание страницы', blank=True, null=True)
    keywords = models.TextField('Ключевые слова', blank=True, null=True)
    start_station = models.CharField('Вокзал отправления туда', max_length=10000, blank=True, null=True)
    aim_station = models.CharField('Вокзал прибытия туда', max_length=10000, blank=True, null=True)
    home_station = models.CharField('Вокзал прибытия оттуда', max_length=10000, blank=True, null=True)
    back_station = models.CharField('Вокзал отправления оттуда', max_length=10000, blank=True, null=True)
    travel_details = models.TextField('Подробности добирания и комментарии',  blank=True, null=True)
    attractions = models.TextField('Достопримечательности',  blank=True, null=True)
    kilometers = models.CharField('Примерный километраж', max_length=10000, blank=True, null=True)
    vk = models.CharField('Ссылка на встречу вк', max_length=10000, blank=True, null=True)
    track = models.CharField('Ссылка на трек', max_length=10000, blank=True, null=True)
    img_track = models.ImageField('Фото трека', upload_to='pictures/static/main/img/', blank=True, null=True,
                                        default='user_images/default1.png')
    dates_try = models.CharField('Даты прохождения', max_length=10000, blank=True, null=True, default='в планах')
    maturity = models.BooleanField(verbose_name='Готов ли маршрут?',
                                           blank=True, null=True, default=False)


    
    
    def __str__(self):
        return f' {self.date} , {self.title}'

    class Meta:
        verbose_name = 'Хайкинг'
        verbose_name_plural = 'Хайкинг'


class Comments(models.Model):
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    text = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Hike, verbose_name='К записи', on_delete=models.PROTECT,
                                related_name='comments')
    author = models.CharField('Автор', max_length=50)

    def __str__(self):
        return f' {self.author} , к {self.forNote.title},  от {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('blogstr', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']
