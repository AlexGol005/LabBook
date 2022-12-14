"""
Модуль проекта LabJournal, приложения equipment.
Приложение equipment это обширное приложение, включает все про лабораторное оборудование и лабораторные помещения
Данный модуль views.py выводит формы для внесения данных пользователями в пользовательской части сайта.
Список блоков:
блок 1 - заглавные страницы с кнопками, структурирующие разделы. (Самая верхняя страница - записана в приложении main)
блок 2 - списки: комнаты, поверители, персоны поверители, производители
блок 3 - списки: Все оборудование, СИ, ИО, ВО, госреестры, характеристики ИО, характеристики ВО
блок 4 - формы регистрации и обновления: комнаты, поверители, персоны поверители, производители, контакты поверителей
блок 5 - микроклимат: журналы, формы регистрации
блок 6 - регистрация госреестры, характеристики, ЛО - внесение, обновление
блок 7 - все поисковики
блок 8 - принадлежности к оборудованию
блок 9 - внесение и обновление поверка и аттестация
блок 10 - индивидуальные страницы СИ ИО ВО их поверок и аттестаций
блок 11 - все комментарии ко всему
блок 12 - вывод списков и форм  для метрологического обеспечения
блок 13 - выгрузка данных в формате ексель
блок 14 - нестандартные exel выгрузки (карточка, протоколы верификации, этикетки)
"""


import xlwt
import pytils.translit
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.db.models import Max, Q, Value, CharField, Count, Sum
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context_processors import request
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from xlwt import Alignment, Borders

from equipment.forms import*
from equipment.models import*
from formstandart import YearForm
from functstandart import get_dateformat
from users.models import Profile

URL = 'equipment'
now = date.today()

# блок 1 - заглавные страницы с кнопками, структурирующие разделы. Самая верхняя страница - в приложении main


class MeteorologicalParametersView(TemplateView):
    """Выводит страницу с кнопками для добавления помещений, микроклимата и вывода журнала микроклимата"""
    template_name = URL + '/meteo.html'


class MetrologicalEnsuringView(TemplateView):
    """Выводит заглавную страницу для Этикетки о поверке/аттестации и списки на поверку/аттестацию """
    template_name = URL + '/metro.html'

    def get_context_data(self, **kwargs):
        context = super(MetrologicalEnsuringView, self).get_context_data(**kwargs)
        context['form'] = DateForm()
        return context


class ReportsView(TemplateView):
    """Выводит страницу с кнопками для вывода планов и отчётов по оборудованию"""
    template_name = URL + '/reports.html'

    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = YearForm()
        return context


# блок 2 - списки: комнаты, поверители, персоны поверители, производители


class VerificatorsView(ListView):
    """ Выводит список всех организаций поверителей """
    model = Verificators
    template_name = 'main/plainlist.html'
    context_object_name = 'objects'


class VerificatorsPersonsView(ListView):
    """ Выводит список всех сотрудников поверителей """
    model = VerificatorPerson
    template_name = 'equipment/verpersonlist.html'
    context_object_name = 'objects'


class ManufacturerView(ListView):
    """ Выводит список всех производителей """
    model = Manufacturer
    template_name = URL + '/manufacturerlist.html'
    context_object_name = 'objects'
    ordering = ['companyName']
    paginate_by = 12


# блок 3 - списки: Все оборудование, СИ, ИО, ВО, госреестры, характеристики ИО, характеристики ВО


class EquipmentView(ListView):
    """ Выводит список Всего ЛО """
    model = Equipment
    template_name = URL + '/equipmentlist.html'
    context_object_name = 'objects'
    ordering = ['exnumber']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EquipmentView, self).get_context_data(**kwargs)
        context['company'] = CompanyCard.objects.get(pk=1).name
        return context


class MeasurEquipmentCharaktersView(ListView):
    """ Выводит список госреестров """
    model = MeasurEquipmentCharakters
    template_name = URL + '/measurequipmentcharacterslist.html'
    context_object_name = 'objects'
    ordering = ['reestr']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MeasurEquipmentCharaktersView, self).get_context_data(**kwargs)
        context['form'] = Searchreestrform()
        return context


class TestingEquipmentCharaktersView(ListView):
    """ Выводит список характеристик ИО """
    model = TestingEquipmentCharakters
    template_name = URL + '/testingequipmentcharacterslist.html'
    context_object_name = 'objects'
    ordering = ['name']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TestingEquipmentCharaktersView, self).get_context_data(**kwargs)
        context['form'] = Searchtestingform()
        return context


class MeasurEquipmentView(ListView):
    """Выводит список средств измерений"""
    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']
    paginate_by = 12

    def get_queryset(self):
        queryset = MeasurEquipment.objects.exclude(equipment__status='С')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MeasurEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context


class TestingEquipmentView(ListView):
    """ Выводит список испытательного оборудования """
    template_name = URL + '/testingequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters__name']
    paginate_by = 12

    def get_queryset(self):
        queryset = TestingEquipment.objects.exclude(equipment__status='С')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TestingEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context


# блок 4 - формы регистрации и обновления: комнаты, поверители, персоны поверители, производители, контакты поверителей

class ContactsVerregView(LoginRequiredMixin, CreateView):
    """ выводит форму добавления контактов поверителей"""
    form_class = ContactsVerForm
    template_name = 'equipment/personverreg.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(ContactsVerregView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить контакт поверителя'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        if form.is_valid():
            order = form.save(commit=False)
            order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
            order.save()
            if order.equipment.kategory == 'СИ':
                return redirect(f'/equipment/measureequipment/verification/{self.kwargs["str"]}')
            if order.equipment.kategory == 'ИО':
                return redirect(f'/equipment/testingequipment/attestation/{self.kwargs["str"]}')


class RoomsCreateView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления помещения """
    template_name = URL + '/reg.html'
    form_class = RoomsCreateForm
    success_url = '/equipment/meteo/'
    success_message = "Помещение успешно добавлено"

    def get_context_data(self, **kwargs):
        context = super(RoomsCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить помещение'
        return context


class VerificatorsCreationView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления компании поверителя """
    template_name = URL + '/reg.html'
    form_class = VerificatorsCreationForm
    success_url = '/equipment/verificators/'
    success_message = "Организация поверитель успешно добавлена"

    def get_context_data(self, **kwargs):
        context = super(VerificatorsCreationView, self).get_context_data(**kwargs)
        context['title'] = 'Внести организацию поверителя'
        return context


class VerificatorPersonCreationView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления сотрудника поверителя """
    template_name = URL + '/reg.html'
    form_class = VerificatorPersonCreationForm
    success_url = '/equipment/verificatorpersons/'
    success_message = "Сотрудник поверитель успешно добавлен"

    def get_context_data(self, **kwargs):
        context = super(VerificatorPersonCreationView, self).get_context_data(**kwargs)
        context['title'] = 'Внести сотрудника поверителя'
        return context


def VerificatorUpdate(request, str):
    """выводит форму для обновления данных о сотруднике поверителе"""
    if request.method == "POST":
        form = VerificatorPersonCreationForm(request.POST,  instance=VerificatorPerson.objects.get(pk=str))
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect('verificatorpersons')
    else:
        form = VerificatorPersonCreationForm(instance=VerificatorPerson.objects.get(pk=str))
    data = {'form': form,
            }
    return render(request, 'equipment/personverreg.html', data)


class ManufacturerRegView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления производителя """
    template_name = URL + '/reg.html'
    form_class = ManufacturerCreateForm
    success_url = '/equipment/manufacturerlist/'
    success_message = "Производитель успешно добавлен"

    def get_context_data(self, **kwargs):
        context = super(ManufacturerRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить производителя ЛО'
        return context


class PersonchangeFormView(View):
    """вывод формы смены ответсвенного за прибор, URL=personchangereg/<str:str>/"""
    def get(self, request, str):
        title = 'Смена ответственного за прибор'
        dop = Equipment.objects.get(exnumber=str)
        form = PersonchangeForm()
        context = {
            'title': title,
            'dop': dop,
            'form': form,
        }
        template_name = 'equipment/reg.html'
        return render(request, template_name, context)

    def post(self, request, str, *args, **kwargs):
        form = PersonchangeForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=str)
                order.save()
                if order.equipment.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipment/{str}')
                if order.equipment.kategory == 'ИО':
                    return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')

        else:
            messages.success(request, f'Раздел для ответственного за поверку приборов')
            return redirect(f'/equipment/measureequipment/{str}')


class RoomschangeFormView(View):
    """вывод формы смены помещения, URL=roomschangereg/<str:str>/"""
    def get(self, request, str):
        title = 'Смена размещения прибора'
        dop = Equipment.objects.get(exnumber=str)
        form = RoomschangeForm()
        context = {
            'title': title,
            'dop': dop,
            'form': form,
        }
        template_name = 'equipment/reg.html'
        return render(request, template_name, context)

    def post(self, request, str, *args, **kwargs):
        form = RoomschangeForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=str)
                order.save()
                if order.equipment.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipment/{str}')
                if order.equipment.kategory == 'ИО':
                    return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')
        else:
            messages.success(request, f'Раздел для ответственного за поверку приборов')
            return redirect(f'/equipment/measureequipment/{str}')


# блок 5 - микроклимат: журналы, формы регистрации
class MeteorologicalParametersCreateView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления метеопараметров """
    template_name = URL + '/reg.html'
    form_class = MeteorologicalParametersRegForm
    success_url = '/equipment/meteo/'
    success_message = "Условия окружающей среды успешно добавлены"

    def get_context_data(self, **kwargs):
        context = super(MeteorologicalParametersCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить условия окружающей среды'
        return context


# блок 6 - регистрация госреестры, характеристики, ЛО - внесение, обновление


@login_required
def EquipmentReg(request):
    """выводит форму для регистрации  ЛО"""
    if request.user.is_superuser:
        if request.method == "POST":
            form = EquipmentCreateForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                try:
                    a = Equipment.objects.filter(exnumber__startswith=order.exnumber).last().exnumber
                    b = int(str(a)[-3::]) + 1
                    c = str(b).rjust(3, '0')
                    d = str(order.exnumber) + c
                    order.exnumber = d
                except:
                    order.exnumber = str(order.exnumber) + '001'
                order.save()
                if order.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipmentreg/{order.exnumber}/')
                if order.kategory == 'ИО':
                    return redirect(f'/equipment/testequipmentreg/{order.exnumber}/')
                else:
                    return redirect('equipmentlist')
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect('equipmentreg')
    else:
        form = EquipmentCreateForm()
        form2 = ManufacturerCreateForm(request.POST)
        # form3 = VerificatorPersonCreationForm(request.POST)
        content = {
            'form': form,
                }
        return render(request, 'equipment/equipmentreg.html', content)


class MeasurEquipmentCharaktersRegView(SuccessMessageMixin, CreateView):
    """ выводит форму внесения госреестра. """
    template_name = URL + '/reg.html'
    form_class = MeasurEquipmentCharaktersCreateForm
    success_url = '/equipment/measurequipmentcharacterslist/'
    success_message = "Госреестр успешно добавлен"

    def get_context_data(self, **kwargs):
        context = super(MeasurEquipmentCharaktersRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить госреестр'
        context['dopin'] = 'equipment/measurequipmentcharacterslist'
        return context


def MeasurEquipmentCharaktersUpdateView(request, str):
    """выводит форму для обновления данных о госреестре"""
    if request.method == "POST":
        form = MeasurEquipmentCharaktersCreateForm(request.POST,
                                                   instance=MeasurEquipmentCharakters.objects.get(pk=str))
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect('measurequipmentcharacterslist')
    else:
        form = MeasurEquipmentCharaktersCreateForm(instance=MeasurEquipmentCharakters.objects.get(pk=str))
    data = {'form': form,
            }
    return render(request, 'equipment/reg.html', data)


class TestingEquipmentCharaktersRegView(SuccessMessageMixin, CreateView):
    """ выводит форму внесения характеристик ИО. """
    template_name = URL + '/reg.html'
    form_class = TestingEquipmentCharaktersCreateForm
    success_url = '/equipment/testingequipmentcharacterslist/'
    success_message = "Характеристики ИО успешно добавлены"

    def get_context_data(self, **kwargs):
        context = super(TestingEquipmentCharaktersRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить характеристики ИО'
        context['dopin'] = 'equipment/testingequipmentcharacterslist'
        return context


def TestingEquipmentCharaktersUpdateView(request, str):
    """выводит форму для обновления данных о характеристиках ИО"""
    if request.method == "POST":
        form = TestingEquipmentCharaktersCreateForm(request.POST,
                                                    instance=TestingEquipmentCharakters.objects.get(pk=str))
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect('testingequipmentcharacterslist')
    else:
        form = TestingEquipmentCharaktersCreateForm(instance=TestingEquipmentCharakters.objects.get(pk=str))
    data = {'form': form,
            }
    return render(request, 'equipment/reg.html', data)


class MeasureequipmentregView(LoginRequiredMixin, CreateView):
    """ выводит форму регистрации СИ на основе ЛО и Госреестра """
    form_class = MeasurEquipmentCreateForm
    template_name = 'equipment/reg.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(MeasureequipmentregView, self).get_context_data(**kwargs)
        context['title'] = 'Зарегистрировать СИ'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
                order.save()
                return redirect(f'/equipment/measureequipment/{self.kwargs["str"]}')
        else:
            messages.success(request, f'Регистрировать может только ответственный за поверку приборов')
            return redirect(reverse('measureequipmentreg', kwargs={'str': self.kwargs['str']}))


class TestingequipmentregView(LoginRequiredMixin, CreateView):
    """ выводит форму регистрации ИО на основе ЛО и характеристик ИО """
    form_class = TestingEquipmentCreateForm
    template_name = 'equipment/reg.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(TestingequipmentregView, self).get_context_data(**kwargs)
        context['title'] = 'Зарегистрировать ИО'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
                order.save()
                return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')
        else:
            messages.success(request, f'Регистрировать может только ответственный за метрологическое '
                                      f'обеспечение приборов')
            return redirect(reverse('testequipmentreg', kwargs={'str': self.kwargs['str']}))


def EquipmentUpdate(request, str):
    """выводит форму для обновления разрешенных полей оборудования ответственному за оборудование"""
    title = Equipment.objects.get(exnumber=str)
    try:
        get_pk = title.personchange_set.latest('pk').pk
        person = Personchange.objects.get(pk=get_pk).person
    except:
        person = 1
    if person == request.user or request.user.is_superuser:
        if request.method == "POST":
            form = EquipmentUpdateForm(request.POST, request.FILES,  instance=Equipment.objects.get(exnumber=str))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                if title.kategory == 'СИ':
                    return redirect(reverse('measureequipment', kwargs={'str': str}))
                if title.kategory == 'ИО':
                    return redirect(reverse('testequipment', kwargs={'str': str}))
                if title.kategory == 'ВО':
                    return redirect(reverse('supequipment', kwargs={'str': str}))
    if person != request.user and not request.user.is_superuser:
        messages.success(request, f' Для внесения записей о приборе нажмите на кнопку ниже:'
                                  f' "Внести запись о приборе и смотреть записи (для всех пользователей)"'
                                  f'. Добавить особенности работы или поменять статус может только ответственный '
                                  f'за прибор или поверку.')

        if title.kategory == 'СИ':
            return redirect(reverse('measureequipment', kwargs={'str': str}))
        if title.kategory == 'ИО':
            return redirect(reverse('testequipment', kwargs={'str': str}))
        if title.kategory == 'ВО':
            return redirect(reverse('supequipment', kwargs={'str': str}))
    else:
        form = EquipmentUpdateForm(instance=Equipment.objects.get(exnumber=str))
    data = {'form': form, 'title': title
            }
    return render(request, 'equipment/individuality.html', data)


# блок 7 - все поисковики

class ReestrsearresView(TemplateView):
    """ Представление, которое выводит результаты поиска по списку госреестров """

    template_name = URL + '/measurequipmentcharacterslist.html'

    def get_context_data(self, **kwargs):
        context = super(ReestrsearresView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        reestr = self.request.GET['reestr']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        reestr = self.request.GET['reestr']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        if name and not reestr:
            objects = MeasurEquipmentCharakters.objects.\
            filter(Q(name__icontains=name)|Q(name__icontains=name1)).order_by('name')
            context['objects'] = objects
        if reestr and not name:
            objects = MeasurEquipmentCharakters.objects.filter(reestr__icontains=reestr)
            context['objects'] = objects
        if reestr and  name:
            objects = MeasurEquipmentCharakters.objects.filter(reestr__icontains=reestr).\
                filter(Q(name__icontains=name)|Q(name__icontains=name1)).order_by('name')
            context['objects'] = objects
        context['form'] = Searchreestrform(initial={'name': name, 'reestr': reestr})
        context['URL'] = URL
        return context


class SearchResultMeasurEquipmentView(TemplateView):
    """ Представление, которое выводит результаты поиска по списку средств измерений """

    template_name = URL + '/measureequipment.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultMeasurEquipmentView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        exnumber = self.request.GET['exnumber']
        lot = self.request.GET['lot']
        dateser = self.request.GET['dateser']
        if dateser:
            delt = datetime.now() - timedelta(days=60 * 24 * 7)

        get_id_actual = Verificationequipment.objects.select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        list_ = list(get_id_actual)
        set = []
        for n in list_:
            set.append(n.get('id_actual'))
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        if name and not lot and not exnumber and not dateser:
            objects = MeasurEquipment.objects.\
            filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).order_by('charakters__name')
            context['objects'] = objects
        if lot and not name  and not exnumber and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and not lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and not lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if lot and name and not exnumber and not dateser:
            objects = MeasurEquipment.objects.\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and not lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot).\
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and exnumber:
            objects = MeasurEquipment.objects. \
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects

        context['form'] = SearchMEForm(initial={'name': name, 'lot': lot, 'exnumber': exnumber, 'dateser': dateser})
        context['URL'] = URL
        return context


class SearchResultTestingEquipmentView(TemplateView):
    """ Представление, которое выводит результаты поиска по списку испытательного оборудования """

    template_name = URL + '/testingequipment.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultTestingEquipmentView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        exnumber = self.request.GET['exnumber']
        lot = self.request.GET['lot']
        dateser = self.request.GET['dateser']
        if dateser:
            delt = datetime.now() - timedelta(days=60 * 24 * 7)

        get_id_actual = TestingEquipment.objects.select_related('equipmentSM_att').values('equipmentSM_att'). \
            annotate(id_actual=Max('id')).values('id_actual')
        list_ = list(get_id_actual)
        set = []
        for n in list_:
            set.append(n.get('id_actual'))

        if name and not lot and not exnumber and not dateser:
            objects = TestingEquipment.objects.\
            filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if lot and not name  and not exnumber and not dateser:
            objects = TestingEquipment.objects.filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and not lot and not dateser:
            objects = TestingEquipment.objects.filter(equipment__exnumber=exnumber).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and lot and not dateser:
            objects = TestingEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and not lot and not dateser:
            objects = TestingEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and lot and not dateser:
            objects = TestingEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if lot and name and not exnumber and not dateser:
            objects = TestingEquipment.objects.\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and not lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot).\
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and exnumber:
            objects = TestingEquipment.objects. \
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects

        context['form'] = SearchMEForm(initial={'name': name, 'lot': lot, 'exnumber': exnumber, 'dateser': dateser})
        context['URL'] = URL
        return context


# блок 8  принадлежности к оборудованию


class DocsConsView(View):
    """ выводит список принадлежностей прибора и форму для добавления принадлежности """
    def get(self, request, str):
        template_name = 'equipment/docsconslist.html'
        form = DocsConsCreateForm()
        title = Equipment.objects.get(exnumber=str)
        objects = DocsCons.objects.filter(equipment__exnumber=str).order_by('pk')
        context = {
                'title': title,
                'form': form,
                'objects': objects,
                }
        return render(request, template_name, context)

    def post(self, request, str, *args, **kwargs):
        form = DocsConsCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.equipment = Equipment.objects.get(exnumber=str)
            order.save()
            return redirect(f'/equipment/docsreg/{str}')


class ChromatoView(TemplateView):
    """ Представление, которое выводит список принадлежностей для хроматографа """
    template_name = URL + '/chromato.html'


# блок 9 - внесение и обновление поверка и аттестация


@login_required
def VerificationReg(request, str):
    """выводит форму для внесения сведений о поверке"""
    title = Equipment.objects.get(exnumber=str)
    if request.user.is_superuser:
        if request.method == "POST":
            form = VerificationRegForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.equipmentSM = MeasurEquipment.objects.get(equipment__exnumber=str)
                order.save()
                return redirect(order)
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('measureequipmentver', kwargs={'str': str}))
    else:
        form = VerificationRegForm()
    data = {
        'form': form,
        'title': title
    }
    return render(request, 'equipment/verificationreg.html', data)


@login_required
def AttestationReg(request, str):
    """выводит форму для внесения сведений об аттестации"""
    title = Equipment.objects.get(exnumber=str)
    if request.user.is_superuser:
        if request.method == "POST":
            form = AttestationRegForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.equipmentSM = TestingEquipment.objects.get(equipment__exnumber=str)
                order.save()
                return redirect(order)
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('testingequipmentatt', kwargs={'str': str}))
    else:
        form = AttestationRegForm()
    data = {
        'form': form,
        'title': title
    }
    return render(request, 'equipment/attestationreg.html', data)


def EquipmentMetrologyUpdate(request, str):
    """выводит форму для обновления постоянных особенностей поверки"""
    title = Equipment.objects.get(exnumber=str)
    try:
        get_pk = title.personchange_set.latest('pk').pk
        person = Personchange.objects.get(pk=get_pk).person
    except:
        person = 1

    if person == request.user or request.user.is_superuser:
        if request.method == "POST":
            form = MetrologyUpdateForm(request.POST, instance=Equipment.objects.get(exnumber=str))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                if title.kategory == 'СИ':
                    return redirect(reverse('measureequipmentver', kwargs={'str': str}))
                if title.kategory == 'ИО':
                    return redirect(reverse('testingequipmentatt', kwargs={'str': str}))
    if person != request.user and not request.user.is_superuser:
        messages.success(request, f'. поменять статус может только ответственный за поверку.')
        return redirect(reverse('measureequipmentver', kwargs={'str': str}))
    else:
        form = MetrologyUpdateForm(instance=Equipment.objects.get(exnumber=str))
    data = {'form': form, 'title': title
            }
    return render(request, 'equipment/metrologyindividuality.html', data)


class VerificationequipmentView(View):
    """ выводит историю поверок и форму для добавления комментария к истории поверок """

    def get(self, request, str):
        note = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        note2 = ContactsVer.objects.filter(equipment__exnumber=str).order_by('-pk')
        try:
            strreg = note.latest('pk').equipmentSM.equipment.exnumber
        except:
            strreg = Equipment.objects.get(exnumber=str).exnumber
        try:
            calinterval = note.latest('pk').equipmentSM.charakters.calinterval
        except:
            calinterval = '-'
        title = Equipment.objects.get(exnumber=str)
        try:
            dateorder = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).last().dateorder
        except:
            dateorder = 'не поверен'
        now = date.today()
        try:
            comment = CommentsVerificationequipment.objects.filter(forNote__exnumber=str).last().note
        except:
            comment = ''
        form = CommentsVerificationCreationForm(initial={'comment': comment})
        data = {'note': note,
                'note2': note2,
                'title': title,
                'calinterval': calinterval,
                'now': now,
                'dateorder': dateorder,
                'form': form,
                'comment': comment,
                'strreg': strreg,
                }
        return render(request, 'equipment/verification.html', data)

    def post(self, request, str, *args, **kwargs):
        form = CommentsVerificationCreationForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.author = request.user
                order.forNote = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(order)
        else:
            messages.success(request, f'Комментировать может только ответственный за поверку приборов')
            return redirect(reverse('measureequipmentver', kwargs={'str': str}))


class AttestationequipmentView(View):
    """ выводит историю аттестаций и форму для добавления комментария к истории аттестаций """

    def get(self, request, str):
        note = Attestationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        note2 = ContactsVer.objects.filter(equipment__exnumber=str).order_by('-pk')
        try:
            strreg = note.latest('pk').equipmentSM.equipment.exnumber
        except:
            strreg = Equipment.objects.get(exnumber=str).exnumber
        try:
            calinterval = note.latest('pk').equipmentSM.charakters.calinterval
        except:
            calinterval = '-'
        title = Equipment.objects.get(exnumber=str)
        try:
            dateorder = Attestationequipment.objects.filter(equipmentSM__equipment__exnumber=str).last().dateorder
        except:
            dateorder = 'не аттестован'
        now = date.today()
        try:
            comment = CommentsAttestationequipment.objects.filter(forNote__exnumber=str).last().note
        except:
            comment = ''
        form = CommentsAttestationequipmentForm(initial={'comment': comment})
        data = {'note': note,
                'note2': note2,
                'title': title,
                'calinterval': calinterval,
                'now': now,
                'dateorder': dateorder,
                'form': form,
                'comment': comment,
                'strreg': strreg,
                }
        return render(request, 'equipment/attestation.html', data)

    def post(self, request, str, *args, **kwargs):
        form = CommentsAttestationequipmentForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.author = request.user
                order.forNote = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(order)
        else:
            messages.success(request, f'Комментировать может только ответственный за поверку приборов')
            return redirect(reverse('testingequipmentattestation', kwargs={'str': str}))


class HaveorderVerView(UpdateView):
    """ выводит форму добавления инфо о заказе поверки """
    template_name = 'equipment/reg.html'
    form_class = OrderMEUdateForm

    def get_object(self, queryset=None):
        queryset_get = Verificationequipment.objects. \
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        q = Verificationequipment.objects.filter(id__in=set). \
            get(equipmentSM_id=self.kwargs['pk'])
        return q


    def get_context_data(self, **kwargs):
        context = super(HaveorderVerView, self).get_context_data(**kwargs)
        context['title'] = "Заказана поверка или новое СИ"
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser:
            order = form.save(commit=False)
            order.save()
            return redirect(f"/equipment/measureequipmentall/")
        else:
            return redirect(f"/equipment/measureequipmentall/")


class HaveorderAttView(UpdateView):
    """ выводит форму добавления инфо о заказе аттестации """
    template_name = 'equipment/reg.html'
    form_class = OrderMEUdateForm

    def get_object(self, queryset=None):
        queryset_get = Attestationequipment.objects. \
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        q = Attestationequipment.objects.filter(id__in=set). \
            get(equipmentSM_id=self.kwargs['pk'])
        return q

    def get_context_data(self, **kwargs):
        context = super(HaveorderAttView, self).get_context_data(**kwargs)
        context['title'] = "Заказана аттестация или новое ИО"
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser:
            order = form.save(commit=False)
            order.save()
            return redirect(f"/equipment/testingequipmentall/")
        else:
            return redirect(f"/equipment/testingequipmentall/")

# блок 10 - индивидуальные страницы СИ ИО ВО их поверок и аттестаций


class StrMeasurEquipmentView(View):
    """ выводит отдельную страницу СИ """
    def get(self, request, str):
        note = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        obj = get_object_or_404(MeasurEquipment, equipment__exnumber=str)
        context = {
            'obj': obj,
            'note': note,
        }
        return render(request, URL + '/equipmentstr.html', context)


class StrTestEquipmentView(View):
    """ выводит отдельную страницу ИО """
    def get(self, request, str):
        note = Attestationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        obj = get_object_or_404(TestingEquipment, equipment__exnumber=str)
        context = {
            'obj': obj,
            'note': note,
        }
        return render(request, URL + '/testingequipmentstr.html', context)


# блок 11 - все комментарии ко всему

class CommentsView(View):
    """ выводит комментарии к оборудованию и форму для добавления комментариев """
    form_class = NoteCreationForm
    initial = {'key': 'value'}
    template_name = 'equipment/comments.html'

    def get(self, request, str):
        note = CommentsEquipment.objects.filter(forNote__exnumber=str).order_by('-pk')
        title = Equipment.objects.get(exnumber=str)
        form = NoteCreationForm()
        return render(request, 'equipment/comments.html', {'note': note, 'title': title, 'form': form, 'URL': URL})

    def post(self, request, str, *args, **kwargs):
        form = NoteCreationForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user and not order.author:
                order.author = request.user
            if not request.user and order.author:
                order.author = order.author
            order.forNote = Equipment.objects.get(exnumber=str)
            order.save()
            messages.success(request, f'Запись добавлена!')
            return redirect(order)


# блок 12 - вывод списков и форм  для метрологического обеспечения
class SearchMustVerView(ListView):
    """ выводит список СИ у которых дата заказа поверки совпадает с указанной либо раньше неё"""

    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchMustVerView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Verificationequipment.objects.filter(haveorder=False).\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Verificationequipment.objects.filter(id__in=set).\
            filter(dateorder__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = MeasurEquipment.objects.filter(id__in=set1).filter(equipment__status='Э')
        return queryset


class SearchNotVerView(ListView):
    """ выводит список СИ у которых дата окончания поверки совпадает с указанной либо раньше неё"""

    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchNotVerView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Verificationequipment.objects.\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Verificationequipment.objects.filter(id__in=set).\
            filter(datedead__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = MeasurEquipment.objects.filter(id__in=set1).exclude(equipment__status='C')
        return queryset


class LastNewEquipmentView(ListView):
    """ выводит список 10 приборов, которые были добавлены последними"""

    template_name = URL + '/equipmentlist.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(LastNewEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        return context

    def get_queryset(self):
        Total = Equipment.objects.count()
        queryset = Equipment.objects.filter()[Total-10:Total]
        return queryset


class SearchMustOrderView(ListView):
    """ выводит список СИ у которых месяц заказа поверки совпадает с указанным либо раньше него"""

    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchMustOrderView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Verificationequipment.objects.filter(haveorder=False).\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Verificationequipment.objects.filter(id__in=set).\
            filter(dateordernew__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = MeasurEquipment.objects.filter(id__in=set1).filter(equipment__status='Э')
        return queryset


class VerificationLabelsView(TemplateView):
    """выводит форму для ввода внутренних номеров для распечатки этикеток о метрологическом обслуживании приборов """
    template_name = URL + '/labels.html'

    def get_context_data(self, **kwargs):
        context = super(VerificationLabelsView, self).get_context_data(**kwargs)
        context['form'] = LabelEquipmentform()
        return context


# -------------------

# блок 13 - выгрузка данных в формате ексель (списки приборов)


# блок получения констант для блока 13 и блока 14
# для фильтрации кверисетов для выгрузок ексель. Так как нужно выбирать актуальные (последниие)
# поверки/аттестации из их таблиц и подставлять их в таблицы СИ и ИО, при этом не теряя остальные поля,
# поэтому просто группировка не подходит
get_id_room = Roomschange.objects.select_related('equipment').values('equipment'). \
        annotate(id_actual=Max('id')).values('id_actual')
list_ = list(get_id_room)
setroom = []
for n in list_:
    setroom.append(n.get('id_actual'))

get_id_person = Personchange.objects.select_related('equipment').values('equipment'). \
        annotate(id_actual=Max('id')).values('id_actual')
list_ = list(get_id_person)
setperson = []
for n in list_:
    setperson.append(n.get('id_actual'))

get_id_verification = Verificationequipment.objects.select_related('equipmentSM').values('equipmentSM'). \
    annotate(id_actual=Max('id')).values('id_actual')
list_ = list(get_id_verification)
setver = []
for n in list_:
    setver.append(n.get('id_actual'))

get_id_attestation = Attestationequipment.objects.select_related('equipmentSM').values('equipmentSM'). \
    annotate(id_actual=Max('id')).values('id_actual')
list_ = list(get_id_attestation)
setatt = []
for n in list_:
    setatt.append(n.get('id_actual'))


# флаг ексели отчёты и планы по приборам
# Набор вьюшек для выгрузки планов и отчетов по оборудованию в exel
# Так как планы и отчеты имеют сходную структуру. Они разделены на страницы для СИ, ИО, ВО,
# а также на помесячные суммы, то
# вначале идет общая базовая  функция.
# В ней объединено все общее для всех планов и отчетов. Базовая функция  выполняется в индивидуальных функциях


def base_planreport_xls(request, exel_file_name,
                               measure_e, testing_e, helping_e,
                               measure_e_months, testing_e_months, helping_e_months,
                               u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6):
    """базовое шаблон представление для выгрузки планов и отчетов по СИ, ИО, ВО
    к которому обращаются частные представления"""

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{exel_file_name}.xls"'

    # стили
    al10 = Alignment()
    al10.horz = Alignment.HORZ_CENTER
    al10.vert = Alignment.VERT_CENTER
    al10.wrap = 1

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.top = 1
    b1.bottom = 1

    # заголовки жирным шрифтом, с границами ячеек
    style_headers = xlwt.XFStyle()
    style_headers.font.bold = True
    style_headers.font.name = 'Times New Roman'
    style_headers.borders = b1
    style_headers.alignment = al10

    # обычные ячейки, с границами ячеек
    style_plain = xlwt.XFStyle()
    style_plain.font.name = 'Times New Roman'
    style_plain.borders = b1
    style_plain.alignment = al10

    # обычные ячейки с датами, с границами ячеек
    style_date = xlwt.XFStyle()
    style_date.font.name = 'Times New Roman'
    style_date.borders = b1
    style_date.alignment = al10
    style_date.num_format_str = 'DD.MM.YYYY'


    # добавляем книгу и страницы
    wb = xlwt.Workbook(encoding='utf-8')
    ws1 = wb.add_sheet(f'{str1}', cell_overwrite_ok=True)
    ws2 = wb.add_sheet(f'{str2}', cell_overwrite_ok=True)
    ws3 = wb.add_sheet(f'{str3}', cell_overwrite_ok=True)
    ws4 = wb.add_sheet(f'{str4}', cell_overwrite_ok=True)
    ws5 = wb.add_sheet(f'{str5}', cell_overwrite_ok=True)
    ws6 = wb.add_sheet(f'{str6}', cell_overwrite_ok=True)

    # убираем колонтитулы
    ws1.header_str = b' '
    ws1.footer_str = b' '
    ws2.header_str = b' '
    ws2.footer_str = b' '
    ws3.header_str = b' '
    ws3.footer_str = b' '
    ws4.header_str = b' '
    ws4.footer_str = b' '
    ws5.header_str = b' '
    ws5.footer_str = b' '
    ws6.header_str = b' '
    ws6.footer_str = b' '

    # ширина столбцов СИ
    ws1.col(0).width = 3000
    ws1.col(1).width = 3000
    ws1.col(2).width = 4500
    ws1.col(3).width = 3000
    ws1.col(4).width = 2000
    ws1.col(6).width = 2600
    ws1.col(7).width = 3000
    ws1.col(8).width = 3000

    # ширина столбцов ИО
    ws2.col(0).width = 3000
    ws2.col(1).width = 4500
    ws2.col(2).width = 3500
    ws2.col(3).width = 4200
    ws2.col(4).width = 3000
    ws2.col(5).width = 2600
    ws2.col(6).width = 3000
    ws2.col(7).width = 3000

    # ширина столбцов ВО
    ws3.col(0).width = 3000
    ws3.col(1).width = 4500
    ws3.col(2).width = 3500
    ws3.col(3).width = 4200
    ws3.col(4).width = 2000
    ws3.col(5).width = 2600
    ws3.col(6).width = 3000
    ws3.col(7).width = 3000

    # колонки для разбиивок по месяцам
    columns_month = [
        'Месяц',
        'Количество единиц оборудования',
        'Сумма, руб',
    ]

    # записываем страницу 1 - СИ
    # заголовки СИ
    row_num = 0
    columns = [
        'Внутренний номер',
        'Номер в госреестре',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
    ]

    columns = columns + u_headers_me

    datecolumnme = []

    # запись заголовков СИ
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style_headers)
        if 'Дата' in str(columns[col_num]) or 'дата' in str(columns[col_num]):
            datecolumnme.append(col_num)

    # данные СИ и их запись
    rows = measure_e
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num in datecolumnme:
                ws1.write(row_num, col_num, row[col_num], style_date)
            else:
                ws1.write(row_num, col_num, row[col_num], style_plain)

    # записываем страницу 2 - ИО
    # заголовки ИО
    row_num = 0
    columns = [
        'Внутренний номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
    ]

    columns = columns + u_headers_te

    datecolumnte = []

    # запись заголовков ИО
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], style_headers)
        if 'Дата' in str(columns[col_num]) or 'дата' in str(columns[col_num]):
            datecolumnte.append(col_num)

    # данные ИО и их запись
    rows = testing_e
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num in datecolumnte:
                ws2.write(row_num, col_num, row[col_num], style_date)
            else:
                ws2.write(row_num, col_num, row[col_num], style_plain)

    # записываем страницу 3 - ВО
    # заголовки ВО
    row_num = 0
    columns = [
        'Внутренний номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
    ]

    columns = columns + u_headers_he

    datecolumnhe = []

    # запись заголовков ВО
    for col_num in range(len(columns)):
        ws3.write(row_num, col_num, columns[col_num], style_headers)
        if 'Дата' in str(columns[col_num]) or 'дата' in str(columns[col_num]):
            datecolumnhe.append(col_num)

    # данные ВО и их запись
    rows = helping_e
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num in datecolumnhe:
                ws3.write(row_num, col_num, row[col_num], style_date)
            else:
                ws3.write(row_num, col_num, row[col_num], style_plain)

    # записываем страницу 4 - подсчёт по месяцам для СИ (ПСИ)
    # заголовки ПСИ
    row_num = 0

    # запись заголовков ПСИ
    for col_num in range(len(columns_month)):
        ws4.write(row_num, col_num, columns_month[col_num], style_headers)

    # данные ПСИ и их запись
    rows = measure_e_months
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws4.write(row_num, col_num, row[col_num], style_plain)

    # записываем страницу 5 - подсчёт по месяцам для ИО (ПИО)
    # заголовки ПИО
    row_num = 0

    # запись заголовков ПИО
    for col_num in range(len(columns_month)):
        ws5.write(row_num, col_num, columns_month[col_num], style_headers)

    # данные ПИО и их запись
    rows = testing_e_months
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws5.write(row_num, col_num, row[col_num], style_plain)

    # записываем страницу 6 - подсчёт по месяцам для ВО (ПВО)
    # заголовки ПВО
    row_num = 0

    # запись заголовков ПВО
    for col_num in range(len(columns_month)):
        ws6.write(row_num, col_num, columns_month[col_num], style_headers)

    # данные ПВО и их запись
    rows = helping_e_months
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws6.write(row_num, col_num, row[col_num], style_plain)

    # все сохраняем
    wb.save(response)
    return response


# флаг гафик поверки и аттестации новыйграфик кошка
def export_me_xls(request):
    """представление для выгрузки плана закупки по поверке и аттестации на указанный год"""
    exel_file_name = f'ver_att_schedule.xls'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 4
    str5 = 5
    str6 = 6


    u_headers_me = [
                'Год выпуска',
                'Новый или б/у',
                'Год ввода в эксплуатацию',
                'Страна, наименование производителя',
                'Место установки или хранения',
                'Ответственный за СИ',
                'Статус',
                'Ссылка на сведения о поверке',
                'Номер свидетельства',
                'Дата поверки/калибровки',
                'Дата окончания свидетельства',
                'Дата заказа поверки/калибровки',
                'Дата заказа замены',
                'Периодичность поверки /калибровки (месяцы)',
                'Инвентарный номер',
               ]

    measure_e = MeasurEquipment.objects.all().\
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
    manuf_country=Concat('equipment__manufacturer__country', Value(', '), 'equipment__manufacturer__companyName')).\
        filter(equipment__roomschange__in=setroom).\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_ver__in=setver).\
        exclude(equipment__status='C').\
        values_list(
            'equipment__exnumber',
            'charakters__reestr',
            'charakters__name',
            'mod_type',
            'equipment__lot',
            'equipment__yearmanuf',
            'equipment__new',
            'equipment__yearintoservice',
            'manuf_country',
            'equipment__roomschange__roomnumber__roomnumber',
            'equipment__personchange__person__username',
            'equipment__status',
            'equipmentSM_ver__arshin',
            'equipmentSM_ver__certnumber',
            'equipmentSM_ver__date',
            'equipmentSM_ver__datedead',
            'equipmentSM_ver__dateorder',
            'equipmentSM_ver__dateordernew',
            'charakters__calinterval',
            'equipment__invnumber',
        )

    u_headers_te = [
        'Год выпуска',
        'Новый или б/у',
        'Год ввода в эксплуатацию',
        'Страна, наименование производителя',
        'Место установки или хранения',
        'Ответственный за ИО',
        'Статус',
        'Номер аттестата',
        'Дата аттестации',
        'Дата окончания аттестации',
        'Дата заказа аттестации',
        'Периодичность аттестации',
        'Инвентарный номер',
        'Аттестован на методики',
    ]

    testing_e = TestingEquipment.objects.all(). \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        exclude(equipment__status='C'). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__yearmanuf',
        'equipment__new',
        'equipment__yearintoservice',
        'manuf_country',
        'equipment__roomschange__roomnumber__roomnumber',
        'equipment__personchange__person__username',
        'equipment__status',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead',
        'equipmentSM_att__dateorder',
        'charakters__calinterval',
        'equipment__invnumber',
        'equipmentSM_att__ndocs',
    )

    u_headers_he = []
    helping_e = []
    measure_e_months = []
    testing_e_months = []
    helping_e_months = []

    return base_planreport_xls(request, exel_file_name,
                               measure_e, testing_e, helping_e,
                               measure_e_months, testing_e_months, helping_e_months,
                               u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6
                               )

# флаг отчёты по поверке
def export_metroyearcust_xls(request):
    """Список СИ и ИО прошедших поверку/аттестацию в указанном году, исключая ЛО купленное с поверкой/аттестацией"""
    serdate = request.GET['date']
    exel_file_name = f'report_inner_metro {serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 'СИ - поверено единиц в месяц'
    str5 = 'ИО - аттестовано единиц в месяц'
    str6 = 6


    u_headers_me = ['Номер свидетельства',
                    'Стоимость поверки, руб.',
                    'Дата поверки/калибровки',
                    'Дата окончания свидетельства',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        exclude(equipmentSM_ver__cust=True). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_ver__certnumber',
        'equipmentSM_ver__price',
        'equipmentSM_ver__date',
        'equipmentSM_ver__datedead',
    ).order_by('equipmentSM_ver__date')

    u_headers_te = ['Номер аттестата',
                    'Стоимость аттестации, руб.',
                    'Дата аттестации',
                    'Дата окончания аттестации',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        exclude(equipmentSM_att__cust=True). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__price',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead'
    ).order_by('equipmentSM_att__date')

    u_headers_he = []
    helping_e = []

    measure_e_months = MeasurEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        filter(equipmentSM_ver__price__isnull=False). \
        exclude(equipmentSM_ver__cust=True). \
        values('equipmentSM_ver__date__month'). \
        annotate(dcount=Count('equipmentSM_ver__date__month'), s=Sum('equipmentSM_ver__price')). \
        order_by(). \
        values_list(
        'equipmentSM_ver__date__month',
        'dcount',
        's',
    )

    testing_e_months = TestingEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        filter(equipmentSM_att__price__isnull=False). \
        exclude(equipmentSM_att__cust=True). \
        values('equipmentSM_att__date__month'). \
        annotate(dcount1=Count('equipmentSM_att__date__month'), s1=Sum('equipmentSM_att__price')). \
        order_by(). \
        values_list(
        'equipmentSM_att__date__month',
        'dcount1',
        's1',
    )

    helping_e_months = []

    return base_planreport_xls(request, exel_file_name,
                        measure_e, testing_e, helping_e,
                       measure_e_months, testing_e_months, helping_e_months,
                        u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6
                               )

def export_metroyearprice_xls(request):
    """представление для выгрузки - Список СИ и ИО прошедших поверку в указанном году только те где
    Список СИ и ИО прошедших поверку в указанном году только где указана стоимость"""
    serdate = request.GET['date']
    exel_file_name = f'report_all_withprice_metro {serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 'СИ - поверено единиц в месяц'
    str5 = 'ИО - аттестовано единиц в месяц'
    str6 = 6


    u_headers_me = ['Номер свидетельства',
                    'Стоимость поверки, руб.',
                    'Дата поверки/калибровки',
                    'Дата окончания свидетельства',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        filter(equipmentSM_ver__price__isnull=False). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_ver__certnumber',
        'equipmentSM_ver__price',
        'equipmentSM_ver__date',
        'equipmentSM_ver__datedead',
    ).order_by('equipmentSM_ver__date')

    u_headers_te = ['Номер аттестата',
                    'Стоимость аттестации, руб.',
                    'Дата аттестации',
                    'Дата окончания аттестации',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        filter(equipmentSM_att__price__isnull=False). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__price',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead'
    ).order_by('equipmentSM_att__date')

    u_headers_he = []
    helping_e = []

    measure_e_months = MeasurEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        filter(equipmentSM_ver__price__isnull=False).\
        values('equipmentSM_ver__date__month').\
        annotate(dcount=Count('equipmentSM_ver__date__month'), s=Sum('equipmentSM_ver__price')).\
        order_by().\
        values_list(
        'equipmentSM_ver__date__month',
        'dcount',
        's',
    )

    testing_e_months = TestingEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        filter(equipmentSM_att__price__isnull=False). \
        values('equipmentSM_att__date__month'). \
        annotate(dcount1=Count('equipmentSM_att__date__month'), s1=Sum('equipmentSM_att__price')). \
        order_by(). \
        values_list(
        'equipmentSM_att__date__month',
        'dcount1',
        's1',
    )

    helping_e_months = []

    return base_planreport_xls(request, exel_file_name,
                        measure_e, testing_e, helping_e,
                       measure_e_months, testing_e_months, helping_e_months,
                        u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6
                               )

def export_metroyear_xls(request):
    """Список СИ и ИО прошедших поверку/аттестацию в указанном году, включая ЛО купленное с поверкой/аттестацие"""
    serdate = request.GET['date']
    exel_file_name = f'report_all_metro {serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 4
    str5 = 5
    str6 = 6


    u_headers_me = ['Номер свидетельства',
                    'Стоимость поверки, руб.',
                    'Дата поверки/калибровки',
                    'Дата окончания свидетельства',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_ver__certnumber',
        'equipmentSM_ver__price',
        'equipmentSM_ver__date',
        'equipmentSM_ver__datedead',
    ).order_by('equipmentSM_ver__date')

    u_headers_te = ['Номер аттестата',
                    'Стоимость аттестации, руб.',
                    'Дата аттестации',
                    'Дата окончания аттестации',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__price',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead'
    ).order_by('equipmentSM_att__date')

    u_headers_he = []
    helping_e = []

    measure_e_months = []

    testing_e_months = []

    helping_e_months = []

    return base_planreport_xls(request, exel_file_name,
                        measure_e, testing_e, helping_e,
                       measure_e_months, testing_e_months, helping_e_months,
                        u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6
                               )

# флаг отчёты по закупке
def export_metronewyear_xls(request):
    """представление для выгрузки -
    Список купленного (введенного в эксплуатацию) СИ и ИО в указанном году"""
    serdate = request.GET['date']
    exel_file_name = f'purchased_equipment_{serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 'ВО'
    str4 = 'Количество СИ в месяц'
    str5 = 'Количество ИО в месяц'
    str6 = 'Количество ВО в месяц'


    u_headers_me = ['Стоимость',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipment__yearintoservice=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__price',
    ).order_by('equipment__date')

    u_headers_te = ['Стоимость',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipment__yearintoservice=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__price',
    ).order_by('equipment__date')

    u_headers_he = ['Стоимость',]
    helping_e = HelpingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__yearintoservice=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__price',
    ).order_by('equipment__date')

    measure_e_months = MeasurEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipment__yearintoservice=serdate). \
        values('equipment__date__month'). \
        annotate(dcount=Count('equipment__date__month'), s=Sum('equipment__price')). \
        order_by(). \
        values_list(
        'equipment__date__month',
        'dcount',
        's',
    )

    testing_e_months = qt1 = TestingEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipment__yearintoservice=serdate). \
        values('equipment__date__month'). \
        annotate(dcount1=Count('equipment__date__month'), s1=Sum('equipment__price')). \
        order_by(). \
        values_list(
        'equipment__date__month',
        'dcount1',
        's1',
    )

    helping_e_months = HelpingEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__yearintoservice=serdate). \
        values('equipment__date__month'). \
        annotate(dcount2=Count('equipment__date__month'), s2=Sum('equipment__price')). \
        order_by(). \
        values_list(
        'equipment__date__month',
        'dcount2',
        's2',
    )

    return base_planreport_xls(request, exel_file_name,
                        measure_e, testing_e, helping_e,
                       measure_e_months, testing_e_months, helping_e_months,
                        u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6
                               )
# флаг план по поверке
def export_planmetro_xls(request):
    """представление для выгрузки плана поверки и аттестации на указанный год"""
    serdate = request.GET['date']
    exel_file_name = f'planmetro {serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 'СИ-количество поверок в месяц'
    str5 = 'ИО-кол-во аттестаций в месяц'
    str6 = 6


    u_headers_me = ['Номер текущего свидетельства',
                    'Стоимость последней поверки, руб. (при наличии)',
                    'Месяц заказа поверки',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
                                filter(equipment__roomschange__in=setroom). \
                                filter(equipment__personchange__in=setperson). \
                                filter(equipmentSM_ver__in=setver). \
                                filter(equipmentSM_ver__dateorder__year=serdate). \
                                values_list(
                                'equipment__exnumber',
                                'charakters__reestr',
                                'charakters__name',
                                'mod_type',
                                'equipment__lot',
                                'equipmentSM_ver__certnumber',
                                'equipmentSM_ver__price',
                                'equipmentSM_ver__dateorder__month',
                            ).order_by('equipmentSM_ver__dateorder__month')

    u_headers_te = ['Номер текущего аттестата',
                    'Стоимость последней аттестации, руб. (при наличии)',
                    'Месяц заказа аттестации',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__dateorder__year=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__price',
        'equipmentSM_att__dateorder__month',
    ).order_by('equipmentSM_att__dateorder__month')

    u_headers_he = []
    helping_e = []
    measure_e_months = MeasurEquipment.objects.\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_ver__dateorder__year=serdate).\
        values('equipmentSM_ver__dateorder__month').\
        annotate(dcount=Count('equipmentSM_ver__dateorder__month'), s=Sum('equipmentSM_ver__price')). \
        order_by().\
        values_list(
        'equipmentSM_ver__dateorder__month',
        'dcount',
        's',
    )

    testing_e_months = TestingEquipment.objects.\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_att__dateorder__year=serdate).\
        values('equipmentSM_att__dateorder__month').\
        annotate(dcount=Count('equipmentSM_att__dateorder__month'), s=Sum('equipmentSM_att__price')). \
        order_by().\
        values_list(
        'equipmentSM_att__dateorder__month',
        'dcount',
        's',
    )
    helping_e_months = []

    return base_planreport_xls(request, exel_file_name,
                               measure_e, testing_e, helping_e,
                               measure_e_months, testing_e_months, helping_e_months,
                               u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6
                               )

# флаг план закупки по поверке
def export_plan_purchaesing_xls(request):
    """представление для выгрузки плана закупки по поверке и аттестации на указанный год"""
    serdate = request.GET['date']
    exel_file_name = f'plan_purchaesing_{serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 'СИ-количество в месяц'
    str5 = 'ИО-кол-во в месяц'
    str6 = 6


    u_headers_me = ['Номер текущего свидетельства',
                    'Стоимость оборудования',
                    'Месяц заказа замены',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
                                filter(equipment__roomschange__in=setroom). \
                                filter(equipment__personchange__in=setperson). \
                                filter(equipmentSM_ver__dateordernew__year=serdate). \
                                filter(equipmentSM_ver__haveorder=False). \
                                values_list(
                                'equipment__exnumber',
                                'charakters__reestr',
                                'charakters__name',
                                'mod_type',
                                'equipment__lot',
                                'equipmentSM_ver__certnumber',
                                'equipment__price',
                                'equipmentSM_ver__dateordernew__month',
                            ).order_by('equipmentSM_ver__dateordernew__month')

    u_headers_te = ['Номер текущего аттестата',
                    'Стоимость оборудования',
                    'Месяц заказа замены',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__dateordernew__year=serdate). \
        filter(equipmentSM_att__haveorder=False). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipment__price',
        'equipmentSM_att__dateordernew__month',
    ).order_by('equipmentSM_att__dateordernew__month')

    u_headers_he = []
    helping_e = []
    measure_e_months = MeasurEquipment.objects.\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_ver__dateordernew__year=serdate). \
        filter(equipmentSM_ver__haveorder=False). \
        values('equipmentSM_ver__dateordernew__month').\
        annotate(dcount=Count('equipmentSM_ver__dateordernew__month'), s=Sum('equipment__price')). \
        order_by().\
        values_list(
        'equipmentSM_ver__dateordernew__month',
        'dcount',
        'dcount',
        's',
    )

    testing_e_months = TestingEquipment.objects.\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_att__dateordernew__year=serdate).\
        values('equipmentSM_att__dateordernew__month').\
        annotate(dcount=Count('equipmentSM_att__dateordernew__month'), s=Sum('equipment__price')). \
        filter(equipmentSM_att__haveorder=False). \
        order_by().\
        values_list(
        'equipmentSM_att__dateordernew__month',
        'dcount',
        's',
    )
    helping_e_months = []

    return base_planreport_xls(request, exel_file_name,
                               measure_e, testing_e, helping_e,
                               measure_e_months, testing_e_months, helping_e_months,
                               u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6
                               )


def export_mustver_xls(request):
    """представление для выгрузки СИ требующих поверки и ИО требующих аттестации"""
    # выборка из ексель по поиску по дате
    serdate = request.GET['date']
    exel_file_name = f'mustveratt_{serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 4
    str5 = 5
    str6 = 6

    queryset_get = Verificationequipment.objects.filter(haveorder=False). \
        select_related('equipmentSM').values('equipmentSM'). \
        annotate(id_actual=Max('id')).values('id_actual')
    b = list(queryset_get)
    set = []
    for i in b:
        a = i.get('id_actual')
        set.append(a)
    queryset_get1 = Verificationequipment.objects.filter(id__in=set). \
        filter(dateorder__lte=serdate).values('equipmentSM__id')
    b = list(queryset_get1)
    set1 = []
    for i in b:
        a = i.get('equipmentSM__id')
        set1.append(a)

    queryset_get0 = Attestationequipment.objects.filter(haveorder=False). \
        select_related('equipmentSM').values('equipmentSM'). \
        annotate(id_actual=Max('id')).values('id_actual')
    b = list(queryset_get0)
    set10 = []
    for i in b:
        a = i.get('id_actual')
        set10.append(a)
    queryset_get10 = Attestationequipment.objects.filter(id__in=set10). \
        filter(dateorder__lte=serdate).values('equipmentSM__id')
    b = list(queryset_get10)
    set10 = []
    for i in b:
        a = i.get('equipmentSM__id')
        set10.append(a)

    u_headers_me = [
                    'Год выпуска',
                    'Место хранения',
                    'Место поверки (предыдущей)',
                    'Сотрудник, ответственный за подготовку к поверке/аттестации',
                    'Постоянное примечание к поверке',
                    ]

    measure_e = MeasurEquipment.objects.filter(id__in=set1). \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__status='Э'). \
        filter(equipmentSM_ver__in=setver). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__yearmanuf',
        'equipment__roomschange__roomnumber__roomnumber',
        'equipmentSM_ver__place',
        'equipment__personchange__person__username',
        'equipment__notemetrology',
    ).order_by('-equipmentSM_ver__place')

    u_headers_te = [
                    'Год выпуска',
                    'Место хранения',
                    'Место аттестации (предыдущей)',
                    'Сотрудник, ответственный за подготовку к поверке/аттестации',
                    'Постоянное примечание к аттестации',
                    ]

    testing_e = TestingEquipment.objects.filter(id__in=set10). \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__status='Э'). \
        filter(equipmentSM_att__in=setatt). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__yearmanuf',
        'equipment__roomschange__roomnumber__roomnumber',
        'equipmentSM_att__place',
        'equipment__personchange__person__username',
        'equipment__notemetrology',
    ).order_by('-equipmentSM_att__place')

    measure_e_months = []
    helping_e = []
    helping_e_months = []
    testing_e_months = []
    u_headers_he = []

    return base_planreport_xls(request, exel_file_name,
                               measure_e, testing_e, helping_e,
                               measure_e_months, testing_e_months, helping_e_months,
                               u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6
                               )


# блок 14 - нестандартные exel выгрузки (карточка, протоколы верификации, этикетки)


def export_mecard_xls(request, pk):
    '''представление для выгрузки карточки на прибор (СИ) в ексель'''
    note = MeasurEquipment.objects.get(pk=pk)
    company = CompanyCard.objects.get(pk=1)
    cardname = pytils.translit.translify(note.equipment.exnumber) + ' ' +\
                pytils.translit.translify(note.charakters.name) +\
                ' ' + pytils.translit.translify(note.equipment.lot)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{cardname}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Основная информация', cell_overwrite_ok=True)

    ws.col(0).width = 2700
    ws.col(1).width = 2500
    ws.col(2).width = 8000
    ws.col(3).width = 3700
    ws.col(4).width = 2500
    ws.col(5).width = 4300
    ws.col(6).width = 4000
    ws.col(7).width = 4300
    ws.col(8).width = 2000
    ws.col(9).width = 2000

    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 0)
    ws.left_margin = 0
    ws.header_str = b'&F c. &P  '
    ws.footer_str = b' '
    ws.start_page_number = 1



    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 26



    al1 = Alignment()
    al1.horz = Alignment.HORZ_CENTER
    al1.vert = Alignment.VERT_CENTER

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.bottom = 1
    b1.top = 1

    style1 = xlwt.XFStyle()
    style1.font.height = 9 * 20
    style1.font.name = 'Calibri'
    style1.alignment = al1
    style1.alignment.wrap = 1
    style1.borders = b1

    style2 = xlwt.XFStyle()
    style2.font.height = 9 * 20
    style2.font.name = 'Calibri'
    style2.alignment = al1
    style2.alignment.wrap = 1
    style2.borders = b1
    style2.pattern = pattern

    style3 = xlwt.XFStyle()
    style3.font.height = 15 * 20
    style3.font.bold = True
    style3.font.name = 'Calibri'
    style3.alignment = al1
    style3.alignment.wrap = 1

    style4 = xlwt.XFStyle()
    style4.font.height = 9 * 20
    style4.font.name = 'Calibri'
    style4.alignment = al1
    style4.alignment.wrap = 1
    style4.borders = b1
    style4.num_format_str = 'DD.MM.YYYY'

    style5 = xlwt.XFStyle()
    style5.font.height = 20 * 20
    style5.font.bold = True
    style5.font.name = 'Calibri'
    style5.alignment = al1
    style5.alignment.wrap = 1

    # for row_num in range(4):
    #     for col_num in range(8):
    #         ws.row(row_num).height_mismatch = True
    #         ws.row(row_num).height = 500

    row_num = 4
    columns = [
        'Регистрационная карточка на СИ и ИО'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(row_num, row_num, 0, 9)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 5
    columns = [
        'Идентификационная и уникальная информация'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 9)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 7
    columns = [
        'Внутренний номер',
        'Номер в госреестре',
        'Наименование',
        'Тип/модификация',
        'Заводской номер',
        'Год выпуска',
        'Производитель',
        'Год ввода в эксплуатацию в ООО "Петроаналитика" ',
        'Новый или б/у',
        'Инвентарный номер',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num = 8
    columns = [
        note.equipment.exnumber,
        note.charakters.reestr,
        note.charakters.name,
        f'{note.charakters.typename}/{note.charakters.modificname}',
        note.equipment.lot,
        note.equipment.yearmanuf,
        f'{note.equipment.manufacturer.country}, {note.equipment.manufacturer.companyName}',
        note.equipment.yearintoservice,
        note.equipment.new,
        note.equipment.invnumber,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num = 9
    columns = [
        'Расположение и комплектность'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 9)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 10
    columns = [
        'Документы, комплектные принадлежности, программное обеспечение',
        'Документы, комплектные принадлежности, программное обеспечение',
        'Документы, комплектные принадлежности, программное обеспечение',
        'Документы, комплектные принадлежности, программное обеспечение',
        'Ответственный за прибор',
        'Ответственный за прибор',
        'Расположение прибора',
        'Расположение прибора',
        'Расположение прибора',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 4, style2)
        ws.merge(row_num, row_num, 5, 6, style2)
        ws.merge(row_num, row_num, 7, 9, style2)

    row_num = 11
    columns = [
        'год появления',
        'наименование документа/комплектной принадлежности/ПО',
        'наименование документа/комплектной принадлежности/ПО',
        'откуда поступил документ/ принадлежность/ПО',
        'откуда поступил документ/ принадлежность/ПО',
        'дата',
        'ответственный, ФИО',
        'дата',
        'номер комнаты',
        'номер комнаты',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 2, style2)
        ws.merge(row_num, row_num, 3, 4, style2)
        ws.merge(row_num, row_num, 8, 9, style2)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    rows_1 = DocsCons.objects.filter(equipment=note.equipment). \
        values_list(
        'date',
        'docs',
        'docs',
        'source',
        'source',
    )
    rows_2 = Personchange.objects.filter(equipment=note.equipment). \
        values_list(
        'date',
        'person__username',
    )

    rows_3 = Roomschange.objects.filter(equipment=note.equipment). \
        values_list(
        'date',
        'roomnumber__roomnumber',
    )


    for row in rows_1:
        row_num += 1
        for col_num in range(5):
            ws.write(row_num, col_num, row[col_num], style1)
            ws.merge(row_num, row_num, 1, 2, style2)
            ws.merge(row_num, row_num, 3, 4, style2)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500
    a = row_num

    row_num = 11
    for row in rows_2:
        row_num += 1
        for col_num in range(5, 7):
            ws.write(row_num, col_num, row[col_num - 5], style4)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500
    b = row_num


    row_num = 11
    for row in rows_3:
        row_num += 1
        for col_num in range(7, 9):
            ws.write(row_num, col_num, row[col_num - 7], style4)
            ws.merge(row_num, row_num, 8, 9, style4)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500
    c = row_num

    d = max(a, b, c)


    row_num = 24
    columns = [
        'Соответствие оборудования  установленным требованиям подтверждается протоколом верификации'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 9, style2)

    ws1 = wb.add_sheet('Данные о ремонте и поверке', cell_overwrite_ok=True)

    ws1.col(0).width = 1500
    ws1.col(1).width = 7000
    ws1.col(2).width = 1000
    ws1.col(3).width = 2400
    ws1.col(4).width = 2000
    ws1.col(5).width = 4000
    ws1.col(6).width = 14000
    ws1.col(7).width = 4000

    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws1.insert_bitmap('logo.bmp', 0, 0)
    ws1.left_margin = 0

    ws1.header_str = b'&F c. &P  '
    ws1.footer_str = b' '
    ws1.start_page_number = 2

    row_num = 4
    columns = [
        'Особенности работы прибора',
        'Особенности работы прибора',
        note.equipment.individuality,
        note.equipment.individuality,
        note.equipment.individuality,
        note.equipment.individuality,
        note.equipment.individuality,
    ]
    for col_num in range(2):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 0, 1, style2)
    for col_num in range(2, len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style1)
        ws1.merge(row_num, row_num, 2, 7, style1)
    ws1.row(row_num).height_mismatch = True
    ws1.row(row_num).height = 2000


    row_num = 6
    columns = [
        'Поверка',
        'Поверка',
        '',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
    ]
    for col_num in range(2):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 0, 1, style2)
    for col_num in range(3, len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 3, 7, style2)

    row_num = 7
    columns = [
        'Год',
        'Сведения о результатах поверки',
        '',
        'Дата',
        'Описание',
        'Описание',
        'Описание',
        'ФИО исполнителя',
    ]
    for col_num in range(2):
        ws1.write(row_num, col_num, columns[col_num], style2)
    for col_num in range(3, len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 4, 6, style2)


    rows_1 = Verificationequipment.objects.filter(equipmentSM__equipment=note.equipment). \
        annotate(ver=Concat(
        Value('Свидетельство о поверке: \n  '),
        'certnumber',
        Value('\n от '), str('date'),
         Value('\n до '), str('datedead'),
        Value('\n выдано '),
        'verificator__companyName', output_field=CharField(),),
    ). \
        annotate(ver_year=Concat(
        'date__year', 'year',
         output_field=CharField(), ),
    ). \
        values_list(
        'ver_year',
        'ver',
    )

    rows_2 = CommentsEquipment.objects.filter(forNote=note.equipment). \
        values_list(
        'date',
        'note',
        'note',
        'note',
        'author',
    )

    for row in rows_1:
        row_num += 1
        for col_num in range(0, 1):
            ws1.write(row_num, col_num, row[col_num], style4)
        for col_num in range(1, 2):
            ws1.write(row_num, col_num, row[col_num], style4)
        ws1.row(row_num).height_mismatch = True
        ws1.row(row_num).height = 1500

    row_num = 7
    for row in rows_2:
        row_num += 1
        for col_num in range(3, 8):
            ws1.write(row_num, col_num, row[col_num - 3], style4)
            ws1.merge(row_num, row_num, 4, 6, style1)
        ws1.row(row_num).height_mismatch = True
        ws1.row(row_num).height = 1500

    wb.save(response)
    return response

# флаг карточки на ИО
def export_tecard_xls(request, pk):
    '''представление для выгрузки карточки на прибор (ИО) в ексель'''
    note = TestingEquipment.objects.get(pk=pk)
    company = CompanyCard.objects.get(pk=1)
    cardname = pytils.translit.translify(note.equipment.exnumber) + ' ' +\
                pytils.translit.translify(note.charakters.name) +\
                ' ' + pytils.translit.translify(note.equipment.lot)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{cardname}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Основная информация', cell_overwrite_ok=True)

    ws.col(0).width = 2700
    ws.col(1).width = 2500
    ws.col(2).width = 8000
    ws.col(3).width = 3700
    ws.col(4).width = 2500
    ws.col(5).width = 4300
    ws.col(6).width = 4000
    ws.col(7).width = 4300
    ws.col(8).width = 2000
    ws.col(9).width = 2000

    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 0)
    ws.left_margin = 0
    ws.header_str = b'&F c. &P  '
    ws.footer_str = b' '
    ws.start_page_number = 1



    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 26



    al1 = Alignment()
    al1.horz = Alignment.HORZ_CENTER
    al1.vert = Alignment.VERT_CENTER

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.bottom = 1
    b1.top = 1

    style1 = xlwt.XFStyle()
    style1.font.height = 9 * 20
    style1.font.name = 'Calibri'
    style1.alignment = al1
    style1.alignment.wrap = 1
    style1.borders = b1

    style2 = xlwt.XFStyle()
    style2.font.height = 9 * 20
    style2.font.name = 'Calibri'
    style2.alignment = al1
    style2.alignment.wrap = 1
    style2.borders = b1
    style2.pattern = pattern

    style3 = xlwt.XFStyle()
    style3.font.height = 15 * 20
    style3.font.bold = True
    style3.font.name = 'Calibri'
    style3.alignment = al1
    style3.alignment.wrap = 1

    style4 = xlwt.XFStyle()
    style4.font.height = 9 * 20
    style4.font.name = 'Calibri'
    style4.alignment = al1
    style4.alignment.wrap = 1
    style4.borders = b1
    style4.num_format_str = 'DD.MM.YYYY'

    style5 = xlwt.XFStyle()
    style5.font.height = 20 * 20
    style5.font.bold = True
    style5.font.name = 'Calibri'
    style5.alignment = al1
    style5.alignment.wrap = 1

    # for row_num in range(4):
    #     for col_num in range(8):
    #         ws.row(row_num).height_mismatch = True
    #         ws.row(row_num).height = 500

    row_num = 4
    columns = [
        'Регистрационная карточка на СИ и ИО'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(row_num, row_num, 0, 9)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 5
    columns = [
        'Идентификационная и уникальная информация'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 9)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 7
    columns = [
        'Внутренний номер',
        'Наименование',
        'Наименование',
        'Тип/модификация',
        'Заводской номер',
        'Год выпуска',
        'Производитель',
        'Год ввода в эксплуатацию в ООО "Петроаналитика" ',
        'Новый или б/у',
        'Инвентарный номер',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 2, style2)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num = 8
    columns = [
        note.equipment.exnumber,
        note.charakters.name,
        note.charakters.name,
        f'{note.charakters.typename}/{note.charakters.modificname}',
        note.equipment.lot,
        note.equipment.yearmanuf,
        f'{note.equipment.manufacturer.country}, {note.equipment.manufacturer.companyName}',
        note.equipment.yearintoservice,
        note.equipment.new,
        note.equipment.invnumber,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 2, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num = 9
    columns = [
        'Расположение и комплектность'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 9)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 10
    columns = [
        'Документы, комплектные принадлежности, программное обеспечение',
        'Документы, комплектные принадлежности, программное обеспечение',
        'Документы, комплектные принадлежности, программное обеспечение',
        'Документы, комплектные принадлежности, программное обеспечение',
        'Ответственный за прибор',
        'Ответственный за прибор',
        'Расположение прибора',
        'Расположение прибора',
        'Расположение прибора',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 4, style2)
        ws.merge(row_num, row_num, 5, 6, style2)
        ws.merge(row_num, row_num, 7, 9, style2)

    row_num = 11
    columns = [
        'год появления',
        'наименование документа/комплектной принадлежности/ПО',
        'наименование документа/комплектной принадлежности/ПО',
        'откуда поступил документ/ принадлежность/ПО',
        'откуда поступил документ/ принадлежность/ПО',
        'дата',
        'ответственный, ФИО',
        'дата',
        'номер комнаты',
        'номер комнаты',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 2, style2)
        ws.merge(row_num, row_num, 3, 4, style2)
        ws.merge(row_num, row_num, 8, 9, style2)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    rows_1 = DocsCons.objects.filter(equipment=note.equipment). \
        values_list(
        'date',
        'docs',
        'docs',
        'source',
        'source',
    )
    rows_2 = Personchange.objects.filter(equipment=note.equipment). \
        values_list(
        'date',
        'person__username',
    )

    rows_3 = Roomschange.objects.filter(equipment=note.equipment). \
        values_list(
        'date',
        'roomnumber__roomnumber',
    )


    for row in rows_1:
        row_num += 1
        for col_num in range(5):
            ws.write(row_num, col_num, row[col_num], style1)
            ws.merge(row_num, row_num, 1, 2, style2)
            ws.merge(row_num, row_num, 3, 4, style2)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500
    a = row_num

    row_num = 11
    for row in rows_2:
        row_num += 1
        for col_num in range(5, 7):
            ws.write(row_num, col_num, row[col_num - 5], style4)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500
    b = row_num


    row_num = 11
    for row in rows_3:
        row_num += 1
        for col_num in range(7, 9):
            ws.write(row_num, col_num, row[col_num - 7], style4)
            ws.merge(row_num, row_num, 8, 9, style4)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500
    c = row_num

    d = max(a, b, c)


    row_num = 24
    columns = [
        'Соответствие оборудования  установленным требованиям подтверждается протоколом верификации'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 9, style2)

    ws1 = wb.add_sheet('Данные о ремонте и аттестации', cell_overwrite_ok=True)

    ws1.col(0).width = 1500
    ws1.col(1).width = 7000
    ws1.col(2).width = 1000
    ws1.col(3).width = 2400
    ws1.col(4).width = 2000
    ws1.col(5).width = 4000
    ws1.col(6).width = 14000
    ws1.col(7).width = 4000

    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws1.insert_bitmap('logo.bmp', 0, 0)
    ws1.left_margin = 0

    ws1.header_str = b'&F c. &P  '
    ws1.footer_str = b' '
    ws1.start_page_number = 2

    row_num = 4
    columns = [
        'Особенности работы прибора',
        'Особенности работы прибора',
        note.equipment.individuality,
        note.equipment.individuality,
        note.equipment.individuality,
        note.equipment.individuality,
        note.equipment.individuality,
    ]
    for col_num in range(2):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 0, 1, style2)
    for col_num in range(2, len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style1)
        ws1.merge(row_num, row_num, 2, 7, style1)
    ws1.row(row_num).height_mismatch = True
    ws1.row(row_num).height = 2000


    row_num = 6
    columns = [
        'Поверка',
        'Поверка',
        '',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
    ]
    for col_num in range(2):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 0, 1, style2)
    for col_num in range(3, len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 3, 7, style2)

    row_num = 7
    columns = [
        'Год',
        'Сведения о результатах аттестации',
        '',
        'Дата',
        'Описание',
        'Описание',
        'Описание',
        'ФИО исполнителя',
    ]
    for col_num in range(2):
        ws1.write(row_num, col_num, columns[col_num], style2)
    for col_num in range(3, len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 4, 6, style2)


    rows_1 = Attestationequipment.objects.filter(equipmentSM__equipment=note.equipment). \
        annotate(ver=Concat(
        Value('Аттестат: \n  '),
        'certnumber',
        Value('\n от '), str('date'),
         Value('\n до '), str('datedead'),
        Value('\n выдан '),
        'verificator__companyName', output_field=CharField(),),
    ). \
        annotate(ver_year=Concat(
        'date__year', 'year',
         output_field=CharField(), ),
    ). \
        values_list(
        'ver_year',
        'ver',
    )

    rows_2 = CommentsEquipment.objects.filter(forNote=note.equipment). \
        values_list(
        'date',
        'note',
        'note',
        'note',
        'author',
    )

    for row in rows_1:
        row_num += 1
        for col_num in range(0, 1):
            ws1.write(row_num, col_num, row[col_num], style4)
        for col_num in range(1, 2):
            ws1.write(row_num, col_num, row[col_num], style4)
        ws1.row(row_num).height_mismatch = True
        ws1.row(row_num).height = 1500

    row_num = 7
    for row in rows_2:
        row_num += 1
        for col_num in range(3, 8):
            ws1.write(row_num, col_num, row[col_num - 3], style4)
            ws1.merge(row_num, row_num, 4, 6, style1)
        ws1.row(row_num).height_mismatch = True
        ws1.row(row_num).height = 1500

    wb.save(response)
    return response


# стили для exel (для этикеток)
brd1 = Borders()
brd1.left = 1
brd1.right = 1
brd1.top = 1
brd1.bottom = 1

al1 = Alignment()
al1.horz = Alignment.HORZ_CENTER
al1.vert = Alignment.VERT_BOTTOM

style1 = xlwt.XFStyle()
style1.font.bold = True
style1.font.name = 'Calibri'
style1.borders = brd1
style1.alignment = al1
style1.alignment.wrap = 1

style2 = xlwt.XFStyle()
style2.font.name = 'Calibri'
style2.borders = brd1
style2.alignment = al1

style3 = xlwt.XFStyle()
style3.font.name = 'Calibri'
style3.alignment = al1

style4 = xlwt.XFStyle()
style4.font.bold = True
style4.font.name = 'Calibri'
style4.alignment = al1

# флаг этикетки СИ
def export_verificlabel_xls(request):
    '''представление для выгрузки этикеток для указания поверки и аттестации'''
    note = []

    for n in (request.GET['n1'], request.GET['n2'],
              request.GET['n3'], request.GET['n4'],
              request.GET['n5'], request.GET['n6'],
              request.GET['n7'], request.GET['n8'],
              request.GET['n9'], request.GET['n10'],
              request.GET['n11'], request.GET['n12'],
              request.GET['n13'], request.GET['n14']):
        try:
            MeasurEquipment.objects.get(equipment__exnumber=n)
            note.append(MeasurEquipment.objects.get(equipment__exnumber=n))
        except:
            pass
        try:
            TestingEquipment.objects.get(equipment__exnumber=n)
            note.append(TestingEquipment.objects.get(equipment__exnumber=n))
        except:
            pass
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="verification_labels.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('1', cell_overwrite_ok=True)
    ws.header_str = b' '
    ws.footer_str = b' '

    # ширина столбцов
    ws.col(0).width = 300
    ws.col(1).width = 3400
    ws.col(2).width = 3600
    ws.col(3).width = 2000
    ws.col(4).width = 2000
    ws.col(5).width = 800
    ws.col(6).width = 3400
    ws.col(7).width = 3600
    ws.col(8).width = 2000
    ws.col(9).width = 2000
    ws.col(10).width = 300


    i = 0
    j = 0
    if len(note) % 2 != 0:
        note.append(note[0])
    while i <= len(note) - 2:
        currentnote1 = note[i]
        currentnote2 = note[i + 1]

        row_num = 0 + j
        columns = [
            '',
            f'{currentnote1.charakters.name} {currentnote1.charakters.typename}/{currentnote1.charakters.modificname}',
            f'{currentnote1.charakters.name} {currentnote1.charakters.typename}/{currentnote1.charakters.modificname}',
            f'{currentnote1.charakters.name} {currentnote1.charakters.typename}/{currentnote1.charakters.modificname}',
            f'{currentnote1.charakters.name} {currentnote1.charakters.typename}/{currentnote1.charakters.modificname}',
            '',
            f'{currentnote2.charakters.name} {currentnote2.charakters.typename}/{currentnote2.charakters.modificname}',
            f'{currentnote2.charakters.name} {currentnote2.charakters.typename}/{currentnote2.charakters.modificname}',
            f'{currentnote2.charakters.name} {currentnote2.charakters.typename}/{currentnote2.charakters.modificname}',
            f'{currentnote2.charakters.name} {currentnote2.charakters.typename}/{currentnote2.charakters.modificname}',
            '',
        ]

        for col_num in (1, 2, 3, 4, 6, 7, 8, 9):
            ws.write(row_num, col_num, columns[col_num], style2)
            ws.merge(row_num, row_num, 1, 4, style2)
            ws.merge(row_num, row_num, 6, 9, style2)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 750

        row_num = 1 + j
        columns = [
            '',
            f'Заводской №:',
            f'{currentnote1.equipment.lot}',
            f'Внут. №',
            f'{currentnote1.equipment.exnumber}',
            '',
            f'Заводской №:',
            f'{currentnote2.equipment.lot}',
            f'Внут. №',
            f'{currentnote2.equipment.exnumber}',
            '',
        ]

        for col_num in (1, 3, 6, 8):
            ws.write(row_num, col_num, columns[col_num], style1)
        for col_num in (2, 4, 7, 9):
            ws.write(row_num, col_num, columns[col_num], style2)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 270

        if currentnote1.equipment.kategory == 'СИ':
            a = 'поверка:'
        if currentnote1.equipment.kategory == 'ИО':
            a = 'аттестация:'
        if currentnote2.equipment.kategory == 'СИ':
            b = 'поверка:'
        if currentnote2.equipment.kategory == 'ИО':
            b = 'аттестация:'

        row_num = 2 + j
        columns = [
            '',
            f'{a}',
            f'{currentnote1.newcertnumber}',
            f'{currentnote1.newcertnumber}',
            f'{currentnote1.newcertnumber}',
            '',
            f'{b}',
            f'{currentnote2.newcertnumber}',
            f'{currentnote2.newcertnumber}',
            f'{currentnote2.newcertnumber}',
            '',
        ]

        for col_num in (1, 6):
            ws.write(row_num, col_num, columns[col_num], style1)
        for col_num in range(2, 5):
            ws.write(row_num, col_num, columns[col_num], style2)
        for col_num in range(7, 10):
            ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 2, 4, style2)
        ws.merge(row_num, row_num, 7, 9, style2)

        if currentnote1.equipment.kategory == 'СИ':
            a = 'поверен'
        if currentnote1.equipment.kategory == 'ИО':
            a = 'аттестован'
        if currentnote2.equipment.kategory == 'СИ':
            b = 'поверен'
        if currentnote2.equipment.kategory == 'ИО':
            b = 'аттестован'

        row_num = 3 + j
        columns = [
            '',
            f'{a} от {currentnote1.newdate} до {currentnote1.newdatedead}',
            f'{a} от {currentnote1.newdate} до {currentnote1.newdatedead}',
            f'{a} от {currentnote1.newdate} до {currentnote1.newdatedead}',
            f'{a} от {currentnote1.newdate} до {currentnote1.newdatedead}',
            ' ',
            f'{b} от {currentnote2.newdate} до {currentnote2.newdatedead}',
            f'{b} от {currentnote2.newdate} до {currentnote2.newdatedead}',
            f'{b} от {currentnote2.newdate} до {currentnote2.newdatedead}',
            f'{b} от {currentnote2.newdate} до {currentnote2.newdatedead}',
            ' ',
            ]
        for col_num in range(1, 5):
            ws.write(row_num, col_num, columns[col_num], style2)
        for col_num in range(6, 10):
            ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 4, style1)
        ws.merge(row_num, row_num, 6, 9, style1)

        if currentnote1.equipment.kategory == 'СИ':
            a = 'поверку'
        if currentnote1.equipment.kategory == 'ИО':
            a = 'аттест-ю:'
        if currentnote2.equipment.kategory == 'СИ':
            b = 'поверку'
        if currentnote2.equipment.kategory == 'ИО':
            b = 'аттест-ю'

        row_num = 4 + j
        columns = [
            '',
            f'Ответственный за {a} {"              "} А.Б.Головкина',
            f'Ответственный за {a} {"              "} А.Б.Головкина',
            f'Ответственный за {a} {"              "} А.Б.Головкина',
            f'Ответственный за {a} {"              "} А.Б.Головкина',
            ' ',
            f'Ответственный за {b} {"              "} А.Б.Головкина',
            f'Ответственный за {b} {"              "} А.Б.Головкина',
            f'Ответственный за {b} {"              "} А.Б.Головкина',
            f'Ответственный за {b} {"              "} А.Б.Головкина',
            ' ',
        ]
        for col_num in range(1, 5):
            ws.write(row_num, col_num, columns[col_num], style2)
        for col_num in range(6, 10):
            ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 4, style1)
        ws.merge(row_num, row_num, 6, 9, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 400

        row_num = 5 + j
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 370

        i += 2
        j += 6

    wb.save(response)
    return response

# флаг верифик
def export_exvercard_xls(request, pk):
    '''представление для выгрузки протокола верификации СИ в ексель'''
    note = MeasurEquipment.objects.get(pk=pk)
    company = CompanyCard.objects.get(pk=1)
    aa = MeasurEquipment.objects.all().filter(equipment__roomschange__in=setroom). \
        values_list('equipment__roomschange__roomnumber__roomnumber').get(pk=pk)
    aa = str(aa)
    room = aa[2:-3]

    bb = MeasurEquipment.objects.all().filter(equipment__personchange__in=setperson). \
        values_list('equipment__personchange__person__username').get(pk=pk)
    bb = str(bb)
    usere = bb[2:-3]
    userelat = pytils.translit.translify(usere)
    positionset = Profile.objects.get(user__username=usere)
    position = positionset.userposition
    cardname = pytils.translit.translify(note.equipment.exnumber) + ' ' + pytils.translit.translify(note.equipment.lot)
    response = HttpResponse(content_type='application/ms-excel')
    filename = f"{userelat}_{cardname}"
    filename = str(filename)
    filename = filename[:251]

    response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'
    # response['Content-Disposition'] = f'attachment; filename="{cardname}.xls"'
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x0D

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Протокол верификации СИ', cell_overwrite_ok=True)

    ws.col(0).width = 2600
    ws.col(1).width = 2500
    ws.col(2).width = 7900
    ws.col(3).width = 3700
    ws.col(4).width = 2500
    ws.col(5).width = 2400
    ws.col(6).width = 3600


    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 0)
    ws.left_margin = 0
    ws.header_str = b'  '
    ws.footer_str = b'c. &P '
    ws.start_page_number = 1

    al1 = Alignment()
    al1.horz = Alignment.HORZ_CENTER
    al1.vert = Alignment.VERT_CENTER

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.bottom = 1
    b1.top = 1

    b5 = Borders()
    b5.left = 5
    b5.right = 5
    b5.bottom = 5
    b5.top = 5

    style1 = xlwt.XFStyle()
    style1.font.height = 9 * 20
    style1.font.name = 'Times new roman'
    style1.alignment = al1
    style1.alignment.wrap = 1
    style1.borders = b1

    style10 = xlwt.XFStyle()
    style10.font.height = 12 * 20
    style10.font.name = 'Times new roman'
    style10.alignment = al1
    style10.alignment.wrap = 1

    style110 = xlwt.XFStyle()
    style110.font.height = 12 * 20
    style110.font.name = 'Times new roman'
    style110.alignment = al1
    style110.alignment.wrap = 1
    style110.pattern = pattern

    style11 = xlwt.XFStyle()
    style11.font.height = 9 * 20
    style11.font.name = 'Times new roman'
    style11.alignment = al1
    style11.alignment.wrap = 1
    style11.borders = b1
    style11.pattern = pattern

    style111 = xlwt.XFStyle()
    style111.font.height = 12 * 20
    style111.font.name = 'Times new roman'
    style111.alignment = al1
    style111.alignment.wrap = 1
    style111.borders = b1

    style2 = xlwt.XFStyle()
    style2.font.height = 9 * 20
    style2.font.name = 'Times new roman'
    style2.alignment = al1
    style2.alignment.wrap = 1
    style2.borders = b1
    style2.pattern = pattern

    style3 = xlwt.XFStyle()
    style3.font.height = 11 * 20
    style3.font.bold = True
    style3.font.name = 'Times new roman'
    style3.alignment = al1
    style3.alignment.wrap = 1

    style4 = xlwt.XFStyle()
    style4.font.height = 9 * 20
    style4.font.name = 'Times new roman'
    style4.alignment = al1
    style4.alignment.wrap = 1
    style4.borders = b1
    style4.num_format_str = 'DD.MM.YYYY'

    style5 = xlwt.XFStyle()
    style5.font.height = 12 * 20
    style5.font.bold = True
    style5.font.name = 'Times new roman'
    style5.alignment = al1
    style5.alignment.wrap = 1

    dateverificformat = now
    dateverific = get_dateformat(now)
    row_num = 4
    columns = [
        f'Протокол верификации № {note.equipment.exnumber}_01/22 от {dateverific} г. СИ вн.№ {note.equipment.exnumber}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 5
    columns = [
        '1. Идентификационная и уникальная информация'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=2
    columns = [
        'Внутренний номер',
        'Номер в госреестре',
        'Наименование',
        'Тип/модификация',
        'Заводской номер',
        'Год выпуска',
        'Производитель',
        # 'Год ввода в эксплуатацию в ООО "Петроаналитика" ',
        # 'Новый или б/у',
        # 'Инвентарный номер',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100


    row_num +=1
    columns = [
        f'СИ {note.equipment.exnumber}',
        note.charakters.reestr,
        note.charakters.name,
        f'{note.charakters.typename}/{note.charakters.modificname}',
        note.equipment.lot,
        note.equipment.yearmanuf,
        f'{note.equipment.manufacturer.country}, {note.equipment.manufacturer.companyName}',
        # note.equipment.yearintoservice,
        # note.equipment.new,
        # note.equipment.invnumber,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num += 2
    columns = [
        'Диапазон измерений',
        'Диапазон измерений',
        'Диапазон измерений',
        'Класс точности, погрешность и/или неопределённость',
        'Класс точности, погрешность и/или неопределённость',
        'Класс точности, погрешность и/или неопределённость',
        'Класс точности, погрешность и/или неопределённость',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 1
    columns = [
        note.charakters.measurydiapason,
        note.charakters.measurydiapason,
        note.charakters.measurydiapason,
        note.charakters.accuracity,
        note.charakters.accuracity,
        note.charakters.accuracity,
        note.charakters.accuracity,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1500

    row_num +=2
    columns = [
        '2. Верификация комплектности и установки оборудования'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '2.1 Соответствие комплектности'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        'Наименование',
        'Наименование',
        'Наименование',
        'Оценка',
        'Примечание',
        'Примечание',
        'Примечание',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.complectlist != '':
        a = note.charakters.complectlist
        st = style1
    else:
        a = 'упаковочный лист'
        st = style11


    row_num += 1
    columns = [
        'Комплектация',
        'Комплектация',
        'Комплектация',
        'cоответствует',
        a,
        a,
        a,
    ]
    for col_num in range(4):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
    for col_num in range(4, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st)
        ws.merge(row_num, row_num, 4, 6, st)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    b = note.equipment.exnumber

    try:
        c = DocsCons.objects.filter(equipment__exnumber=b)
        d = c.filter(docs__icontains='аспорт')
        d = d[0]
        a = 'в наличии'
    except:
        a = 'отсутствует'


    row_num +=1
    columns = [
        'Паспорт',
        'Паспорт',
        'Паспорт',
        a,
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    try:
        c = DocsCons.objects.filter(equipment__exnumber=b)
        d = c.filter(Q(docs__icontains='уководство')|Q(docs__icontains='нструкция')|Q(docs__icontains='ИНСТРУКЦИЯ')|Q(docs__icontains='аспорт'))
        d = d[0]
        a = 'в наличии'
        e = ''
    except:
        a = 'отсутствует'
        e = 'необходимо разработать инструкцию на оборудование'

    row_num += 1
    columns = [
        'Руководство по эксплуатации',
        'Руководство по эксплуатации',
        'Руководство по эксплуатации',
        a,
        e,
        e,
        e,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Сведения о поверке',
        'Сведения о поверке',
        'Сведения о поверке',
        f'поверен до {note.newdatedead}',
        f'№ {note.newcertnumber}',
        f'№ {note.newcertnumber}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500


    try:
        microclimat = MeteorologicalParameters.objects.get(roomnumber__roomnumber=room, date=dateverificformat)
        facttemperature = microclimat.temperature
        facthumid = microclimat.humidity
        factpress = microclimat.pressure
    except:
        facttemperature = 'указать'
        facthumid = 'указать'
        factpress = 'указать'




    row_num +=2
    columns = [
        f'2.2 Соответствие  требованиям к условиям эксплуатации в помещении № {room}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Наименование характеристики',
        'Наименование характеристики',
        'Требования руководства по эксплуатации, паспорта или описания типа',
        'Состояние на момент верификации',
        'Состояние на момент верификации',
        'Оценка',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 1, style1)
        ws.merge(row_num, row_num, 3, 4, style1)
        ws.merge(row_num, row_num, 5, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.power == True:
        row_num += 1
        columns = [
            'Соответствие требованиям к  электропитанию'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style1)
            ws.merge(row_num, row_num, 0, 6, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

        if note.charakters.voltage == '':
            note.charakters.voltage = '-'
            st = style11
        else:
            st = style1



        row_num += 1
        columns = [
            'Напряжение питания сети, В',
            'Напряжение питания сети, В',
            note.charakters.voltage,
            '220',
            '220',
            'соответствует',
        ]
        for col_num in range(3):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 1, st)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 3, 4, st)
            ws.merge(row_num, row_num, 5, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

        if note.charakters.frequency == '':
            note.charakters.frequency = '-'
            st = style11
        else:
            st = style1

        row_num += 1
        columns = [
            'Частота, Гц',
            'Частота, Гц',
            note.charakters.frequency,
            '50',
            '50',
            'соответствует',
        ]
        for col_num in range(3):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 1, st)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 3, 4, st)
            ws.merge(row_num, row_num, 5, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Соответствие требованиям к  микроклимату'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.temperature == '':
        note.charakters.temperature = '-'
        st1 = style11
    else:
        st1 = style1
    if facttemperature == 'указать':
        st3 = style11
    else:
        st3 = style1


    row_num += 1
    columns = [
        'Диапазон рабочих температур, °С',
        'Диапазон рабочих температур, °С',
        note.charakters.temperature,
        facttemperature,
        facttemperature,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.humidicity == '':
        note.charakters.humidicity = '-'
        st1 = style11
    else:
        st1 = style1
    if facthumid == 'указать':
        st3 = style11
    else:
        st3 = style1

    row_num += 1
    columns = [
        'Относительная влажность воздуха, %',
        'Относительная влажность воздуха, %',
        note.charakters.humidicity,
        facthumid,
        facthumid,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.pressure == '':
        note.charakters.pressure = '-'
        st1 = style11
    else:
        st1 = style1

    if factpress == 'указать':
        st3 = style11
    else:
        st3 = style1

    row_num += 1
    columns = [
        'Атмосферное давление, кПа',
        'Атмосферное давление, кПа',
        note.charakters.pressure,
        factpress,
        factpress,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '2.3 Соответствие  установки на рабочем месте требованиям документации на оборудование'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.needsetplace:
        a = ''
        b = '✓'
    if not note.charakters.needsetplace:
        a = '✓'
        b = ''


    row_num += 1
    columns = [
        a,
        'Установка не требуется'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700


    row_num += 1
    columns = [
        b,
        'Требуется установка'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    if note.charakters.needsetplace:
        if not note.charakters.setplace:
            st = style11
        else:
            st = style1


        row_num += 2
        columns = [
            'Описание установки'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style3)
            ws.merge(row_num, row_num, 0, 6)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500


        row_num += 1
        columns = [
              note.charakters.setplace
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500



    row_num += 2
    columns = [
        '3. Тестирование при внедрении оборудования'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.expresstest:
        a = ''
        b = '✓'
    if not note.charakters.expresstest:
        a = '✓'
        b = ''

    row_num += 1
    columns = [
        a,
        'Тестирование невозможно'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 1
    columns = [
        b,
        'Тестирование возможно. Результаты испытаний в приложении 1'

    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 2
    columns = [
        '4. Заключение по результатам верификации'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500


    row_num += 1
    columns = [
        f'Пригодно к эксплуатации.  Требования к установке и условиям окружающей среды соответствуют документации на оборудование.\
        \n Закреплено за помещением № {room}.\n Закреплено за ответственным пользователем: {usere}.'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1500

    row_num += 2
    columns = [
        '',
        '',
        'Верификацию провел:'
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if usere != 'А.Б.Головкина':
        st = style10
    else:
        st = style10

    row_num += 2
    columns = [
        '',
        '',
        position,
        '',
       usere,
       usere,
       usere,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], st)
        ws.merge(row_num, row_num, 4, 6, st)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'Согласовано:'
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'начальник производства'
        '',
        '',
        'Н.Ю.Пилявская',
        'Н.Ю.Пилявская',
        'Н.Ю.Пилявская',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(row_num, row_num, 4, 6, style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'заведующий АХЧ'
        '',
        '',
        'А.В.Теленков',
        'А.В.Теленков',
        'А.В.Теленков',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(row_num, row_num, 4, 6, style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if usere != 'А.Б.Головкина':

        row_num += 2
        columns = [
            '',
            '',
            'инженер-химик 2 категории'
            '',
            '',
            'А.Б.Головкина',
            'А.Б.Головкина',
            'А.Б.Головкина',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style10)
            ws.merge(row_num, row_num, 4, 6, style10)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500


    wb.save(response)
    return response

# флаг верификация ио
def export_exvercardteste_xls(request, pk):
    '''представление для выгрузки протокола верификации ИО в ексель'''
    note = TestingEquipment.objects.get(pk=pk)
    company = CompanyCard.objects.get(pk=1)
    aa = TestingEquipment.objects.all().filter(equipment__roomschange__in=setroom). \
        values_list('equipment__roomschange__roomnumber__roomnumber').get(pk=pk)
    aa = str(aa)
    room = aa[2:-3]

    bb = TestingEquipment.objects.all().filter(equipment__personchange__in=setperson). \
        values_list('equipment__personchange__person__username').get(pk=pk)
    bb = str(bb)
    usere = bb[2:-3]
    userelat = pytils.translit.translify(usere)
    positionset = Profile.objects.get(user__username=usere)
    position = positionset.userposition
    cardname = pytils.translit.translify(note.equipment.exnumber) + ' ' + pytils.translit.translify(note.equipment.lot)
    response = HttpResponse(content_type='application/ms-excel')
    filename = f"{userelat}_{cardname}"
    filename = str(filename)
    filename = filename[:251]

    response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'
    # response['Content-Disposition'] = f'attachment; filename="{cardname}.xls"'
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x0D

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Протокол верификации ИО', cell_overwrite_ok=True)

    ws.col(0).width = 2600
    ws.col(1).width = 2500
    ws.col(2).width = 7900
    ws.col(3).width = 3700
    ws.col(4).width = 2500
    ws.col(5).width = 2400
    ws.col(6).width = 3600


    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 0)
    ws.left_margin = 0
    ws.header_str = b'  '
    ws.footer_str = b'c. &P '
    ws.start_page_number = 1

    al1 = Alignment()
    al1.horz = Alignment.HORZ_CENTER
    al1.vert = Alignment.VERT_CENTER

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.bottom = 1
    b1.top = 1

    b5 = Borders()
    b5.left = 5
    b5.right = 5
    b5.bottom = 5
    b5.top = 5

    style1 = xlwt.XFStyle()
    style1.font.height = 9 * 20
    style1.font.name = 'Times new roman'
    style1.alignment = al1
    style1.alignment.wrap = 1
    style1.borders = b1

    style10 = xlwt.XFStyle()
    style10.font.height = 12 * 20
    style10.font.name = 'Times new roman'
    style10.alignment = al1
    style10.alignment.wrap = 1

    style110 = xlwt.XFStyle()
    style110.font.height = 12 * 20
    style110.font.name = 'Times new roman'
    style110.alignment = al1
    style110.alignment.wrap = 1
    style110.pattern = pattern

    style11 = xlwt.XFStyle()
    style11.font.height = 9 * 20
    style11.font.name = 'Times new roman'
    style11.alignment = al1
    style11.alignment.wrap = 1
    style11.borders = b1
    style11.pattern = pattern

    style111 = xlwt.XFStyle()
    style111.font.height = 12 * 20
    style111.font.name = 'Times new roman'
    style111.alignment = al1
    style111.alignment.wrap = 1
    style111.borders = b1

    style2 = xlwt.XFStyle()
    style2.font.height = 9 * 20
    style2.font.name = 'Times new roman'
    style2.alignment = al1
    style2.alignment.wrap = 1
    style2.borders = b1
    style2.pattern = pattern

    style3 = xlwt.XFStyle()
    style3.font.height = 11 * 20
    style3.font.bold = True
    style3.font.name = 'Times new roman'
    style3.alignment = al1
    style3.alignment.wrap = 1

    style4 = xlwt.XFStyle()
    style4.font.height = 9 * 20
    style4.font.name = 'Times new roman'
    style4.alignment = al1
    style4.alignment.wrap = 1
    style4.borders = b1
    style4.num_format_str = 'DD.MM.YYYY'

    style5 = xlwt.XFStyle()
    style5.font.height = 12 * 20
    style5.font.bold = True
    style5.font.name = 'Times new roman'
    style5.alignment = al1
    style5.alignment.wrap = 1

    dateverificformat = now
    dateverific = get_dateformat(now)
    row_num = 4
    columns = [
        f'Протокол верификации № {note.equipment.exnumber}_01/22 от {dateverific} г. ИО вн.№ {note.equipment.exnumber}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 5
    columns = [
        '1. Идентификационная и уникальная информация'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=2
    columns = [
        'Внутренний номер',
        'Наименование',
        'Наименование',
        'Тип/модификация',
        'Заводской номер',
        'Год выпуска',
        'Производитель',
        # 'Год ввода в эксплуатацию в ООО "Петроаналитика" ',
        # 'Новый или б/у',
        # 'Инвентарный номер',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 2, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100


    row_num +=1
    columns = [
        f'СИ {note.equipment.exnumber}',
        note.charakters.name,
        note.charakters.name,
        f'{note.charakters.typename}/{note.charakters.modificname}',
        note.equipment.lot,
        note.equipment.yearmanuf,
        f'{note.equipment.manufacturer.country}, {note.equipment.manufacturer.companyName}',
        # note.equipment.yearintoservice,
        # note.equipment.new,
        # note.equipment.invnumber,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 2, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num += 2
    columns = [
        'Основные технические характеристики',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 1
    columns = [
        note.charakters.measurydiapason,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1700

    row_num +=2
    columns = [
        '2. Верификация комплектности и установки оборудования'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '2.1 Соответствие комплектности'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        'Наименование',
        'Наименование',
        'Наименование',
        'Оценка',
        'Примечание',
        'Примечание',
        'Примечание',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.complectlist != '':
        a = note.charakters.complectlist
        st = style1
    else:
        a = 'упаковочный лист'
        st = style11


    row_num += 1
    columns = [
        'Комплектация',
        'Комплектация',
        'Комплектация',
        'cоответствует',
        a,
        a,
        a,
    ]
    for col_num in range(4):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
    for col_num in range(4, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st)
        ws.merge(row_num, row_num, 4, 6, st)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    b = note.equipment.exnumber

    try:
        c = DocsCons.objects.filter(equipment__exnumber=b)
        d = c.filter(docs__icontains='аспорт')
        d = d[0]
        a = 'в наличии'
    except:
        a = 'отсутствует'


    row_num +=1
    columns = [
        'Паспорт',
        'Паспорт',
        'Паспорт',
        a,
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    try:
        c = DocsCons.objects.filter(equipment__exnumber=b)
        d = c.filter(Q(docs__icontains='уководство')|Q(docs__icontains='нструкция')|Q(docs__icontains='ИНСТРУКЦИЯ')|Q(docs__icontains='аспорт'))
        d = d[0]
        a = 'в наличии'
        e = ''
    except:
        a = 'отсутствует'
        e = 'необходимо разработать инструкцию на оборудование'

    row_num += 1
    columns = [
        'Руководство по эксплуатации',
        'Руководство по эксплуатации',
        'Руководство по эксплуатации',
        a,
        e,
        e,
        e,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Сведения об аттестации',
        'Сведения об аттестации',
        'Сведения об аттестации',
        f'аттестован до {note.newdatedead}',
        f'№ {note.newcertnumber}',
        f'№ {note.newcertnumber}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500


    try:
        microclimat = MeteorologicalParameters.objects.get(roomnumber__roomnumber=room, date=dateverificformat)
        facttemperature = microclimat.temperature
        facthumid = microclimat.humidity
        factpress = microclimat.pressure
    except:
        facttemperature = 'указать'
        facthumid = 'указать'
        factpress = 'указать'




    row_num +=2
    columns = [
        f'2.2 Соответствие  требованиям к условиям эксплуатации в помещении № {room}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Наименование характеристики',
        'Наименование характеристики',
        'Требования руководства по эксплуатации, паспорта или описания типа',
        'Состояние на момент верификации',
        'Состояние на момент верификации',
        'Оценка',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 1, style1)
        ws.merge(row_num, row_num, 3, 4, style1)
        ws.merge(row_num, row_num, 5, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.power == True:
        row_num += 1
        columns = [
            'Соответствие требованиям к  электропитанию'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style1)
            ws.merge(row_num, row_num, 0, 6, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

        if note.charakters.voltage == '':
            note.charakters.voltage = '-'
            st = style11
        else:
            st = style1



        row_num += 1
        columns = [
            'Напряжение питания сети, В',
            'Напряжение питания сети, В',
            note.charakters.voltage,
            '220',
            '220',
            'соответствует',
        ]
        for col_num in range(3):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 1, st)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 3, 4, st)
            ws.merge(row_num, row_num, 5, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

        if note.charakters.frequency == '':
            note.charakters.frequency = '-'
            st = style11
        else:
            st = style1

        row_num += 1
        columns = [
            'Частота, Гц',
            'Частота, Гц',
            note.charakters.frequency,
            '50',
            '50',
            'соответствует',
        ]
        for col_num in range(3):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 1, st)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 3, 4, st)
            ws.merge(row_num, row_num, 5, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Соответствие требованиям к  микроклимату'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.temperature == '':
        note.charakters.temperature = '-'
        st1 = style11
    else:
        st1 = style1
    if facttemperature == 'указать':
        st3 = style11
    else:
        st3 = style1


    row_num += 1
    columns = [
        'Диапазон рабочих температур, °С',
        'Диапазон рабочих температур, °С',
        note.charakters.temperature,
        facttemperature,
        facttemperature,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.humidicity == '':
        note.charakters.humidicity = '-'
        st1 = style11
    else:
        st1 = style1
    if facthumid == 'указать':
        st3 = style11
    else:
        st3 = style1

    row_num += 1
    columns = [
        'Относительная влажность воздуха, %',
        'Относительная влажность воздуха, %',
        note.charakters.humidicity,
        facthumid,
        facthumid,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.pressure == '':
        note.charakters.pressure = '-'
        st1 = style11
    else:
        st1 = style1

    if factpress == 'указать':
        st3 = style11
    else:
        st3 = style1

    row_num += 1
    columns = [
        'Атмосферное давление, кПа',
        'Атмосферное давление, кПа',
        note.charakters.pressure,
        factpress,
        factpress,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '2.3 Соответствие  установки на рабочем месте требованиям документации на оборудование'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.needsetplace:
        a = ''
        b = '✓'
    if not note.charakters.needsetplace:
        a = '✓'
        b = ''


    row_num += 1
    columns = [
        a,
        'Установка не требуется'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700


    row_num += 1
    columns = [
        b,
        'Требуется установка'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    if note.charakters.needsetplace:
        if not note.charakters.setplace:
            st = style11
        else:
            st = style1


        row_num += 2
        columns = [
            'Описание установки'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style3)
            ws.merge(row_num, row_num, 0, 6)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500


        row_num += 1
        columns = [
              note.charakters.setplace
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500



    row_num += 2
    columns = [
        '3. Тестирование при внедрении оборудования'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.expresstest:
        a = ''
        b = '✓'
    if not note.charakters.expresstest:
        a = '✓'
        b = ''

    row_num += 1
    columns = [
        a,
        'Тестирование невозможно'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 1
    columns = [
        b,
        'Тестирование возможно. Результаты испытаний в приложении 1'

    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 2
    columns = [
        '4. Заключение по результатам верификации'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500


    row_num += 1
    columns = [
        f'Пригодно к эксплуатации.  Требования к установке и условиям окружающей среды соответствуют документации на оборудование.\
        \n Закреплено за помещением № {room}.\n Закреплено за ответственным пользователем: {usere}.'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1500

    row_num += 2
    columns = [
        '',
        '',
        'Верификацию провел:'
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if usere != 'А.Б.Головкина':
        st = style10
    else:
        st = style10

    row_num += 2
    columns = [
        '',
        '',
        position,
        '',
       usere,
       usere,
       usere,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], st)
        ws.merge(row_num, row_num, 4, 6, st)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'Согласовано:'
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'начальник производства'
        '',
        '',
        'Н.Ю.Пилявская',
        'Н.Ю.Пилявская',
        'Н.Ю.Пилявская',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(row_num, row_num, 4, 6, style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'заведующий АХЧ'
        '',
        '',
        'А.В.Теленков',
        'А.В.Теленков',
        'А.В.Теленков',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(row_num, row_num, 4, 6, style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if usere != 'А.Б.Головкина':

        row_num += 2
        columns = [
            '',
            '',
            'инженер-химик 2 категории'
            '',
            '',
            'А.Б.Головкина',
            'А.Б.Головкина',
            'А.Б.Головкина',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style10)
            ws.merge(row_num, row_num, 4, 6, style10)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500


    wb.save(response)
    return response


