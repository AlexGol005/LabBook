from django import forms
from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib

from ckeditor_uploader.widgets import CKEditorUploadingWidget

# история Карелии классы для отображения в админке

# класс для загрузки/выгрузки Карелия
class KareliahistoryResource(resources.ModelResource):
    class Meta:
        model = Kareliahistory


# класс добавления стилей к окну текст карелия
class KareliahistoryAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = Kareliahistory
        fields = '__all__'
        
# класс подробностей Карелия   
class KareliahistoryAdmin(ImportExportActionModelAdmin):
    resource_class = KareliahistoryResource
    list_display = ('pk', 'text',)
    search_fields = ['pk', 'title', 'text']
    form = KareliahistoryAdminForm
        
# фиксация формы в админке Карелия
admin.site.register(Kareliahistory, KareliahistoryAdmin)

# закладки по айти классы для отображения в админке

# класс для загрузки/выгрузки Айти
class ITResource(resources.ModelResource):
    class Meta:
        model = Itbookmarks

# класс добавления стилей к окну текст Айти
class ITAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = Itbookmarks
        fields = '__all__'

# класс подробностей Айти   
class ITAdmin(ImportExportActionModelAdmin):
    resource_class = ITResource
    list_display = ('pk', 'type',)
    search_fields = ['pk', 'title', 'text']
    form = ITAdminForm

# фиксация формы в админке Айти
admin.site.register(Itbookmarks, ITAdmin)

# закладки по айти классы для отображения в админке

# класс для загрузки/выгрузки хайкинг
class HikeResource(resources.ModelResource):
    class Meta:
        model = Hike

# класс добавления стилей к окну текст хайкинг
class HikeAdminForm(forms.ModelForm):
    travel_details = forms.CharField(label="Подробности", widget=CKEditorUploadingWidget())
    class Meta:
        model = Hike
        fields = '__all__'

# класс подробностей хайкинг   
class HikeAdmin(ImportExportActionModelAdmin):
    resource_class = HikeResource
    list_display = ('pk', 'title', )
    search_fields = ['pk', 'title', 'attractions']
    form = HikeAdminForm

# фиксация формы в админке хайкинг
admin.site.register(Hike, HikeAdmin)

# закладки по темам классы для отображения в админке

# класс для загрузки/выгрузки закладки по темам
class BookmarksResource(resources.ModelResource):
    class Meta:
        model = Bookmarks

# класс добавления стилей к окну текст закладки по темам
class BookmarksAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = Bookmarks
        fields = '__all__'

# класс подробностей закладки по темам   
class BookmarksAdmin(ImportExportActionModelAdmin):
    resource_class = BookmarksResource
    list_display = ('pk', 'text')
    search_fields = ['pk', 'text']
    form = BookmarksAdminForm

# фиксация формы в админке закладки по темам
admin.site.register(Bookmarks, BookmarksAdmin)
