"""
Модуль проекта LabJournal, приложения kinematicviscosity.
Приложение kinematicviscosity это журнал фиксации
лабораторных записей по измерению кинематической вязкости нефтепродуктов
(Лабортаорный журнал измерения кинематической вязкости).

Данный модуль constants.py содержит константы характерные для данного приложения (журнала).
"""

from main.models import AttestationJ

# критерий округления результата
# ROUND = (
#          ('ГОСТ 33768-2015', 'ГОСТ 33768-2015. Метод определения кинематической вязкости и '
#           'расчет динамической вязкости прозрачных и непрозрачных жидкостей'),
#          ('оценка', 'оценка вязкости'),
#          ('ГОСТ 33-2016', 'ГОСТ 33-2016.НЕФТЬ И НЕФТЕПРОДУКТЫ. ПРОЗРАЧНЫЕ И НЕПРОЗРАЧНЫЕ ЖИДКОСТИ.'
#           ' Определение кинематической и динамической вязкости'),)

RELEERROR = 0.01  # критерий округления результата для гост 33768

# нормативные документы по которым проводятся работы
ndocumentoptional = (
                     ('ГОСТ 33768-2015', 'ГОСТ 33768-2015. Метод определения кинематической вязкости и '
                      'расчет динамической вязкости прозрачных и непрозрачных жидкостей'),
                     ('оценка', 'оценка вязкости'),
                     ('ГОСТ 33-2016', 'ГОСТ 33-2016.НЕФТЬ И НЕФТЕПРОДУКТЫ. ПРОЗРАЧНЫЕ И НЕПРОЗРАЧНЫЕ ЖИДКОСТИ.'
                      ' Определение кинематической и динамической вязкости'),)

# Показатели прецизионности
# состав пробы
CHOICES = (
    ('1', 'Прочие нефтепродукты'),
    ('2', 'Базовые масла при 40°С и 100°С'),
    ('3', 'Компаундированные масла при 40°С и 100°С'),
    ('5', 'Нефтяные парафины при 100°С'),
    ('6', 'Другое'),
)

# повторяемость
REPEATABILITY = (
    ('1', '0.35'),
    ('2', '0.11'),
    ('3', '0.26'),
    ('5', '1.41'),
    ('6', '0.35'),
)

JOURNAL = AttestationJ
journal = 'attestationJ'
URL = 'kinematicviscosity'
NAME = 'кинематика'


# для выгрузок протоколов в exel
parameter = 'кинематическая вязкость'
conclusion = 'Контроль повторяемости результатов измерений кинематической вязкости удовлетворителен, ' \
             'так как расхождение между результатами измерений кинематической вязкости в условиях ' \
             'повторяемости не превышает норматив контроля'


