from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


class ProductResource(resources.ModelResource):
    #category = fields.Field(column_name='title', attribute='title')
    class Meta:
        model = Kareliahistory
        
class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = [field.name for field in Kareliahistory._meta.fields if field.name != "id"]



@admin.register(Itbookmarks)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'type',)
    search_fields = ['pk']

@admin.register(Bookmarks)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text')
    search_fields = ['pk', 'text']
    
@admin.register(Hike)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', )

    search_fields = ['pk', 'title', 'attractions']

#@admin.register(Kareliahistory)
#class NoteAdmin(admin.ModelAdmin):
    #list_display = ('pk', 'title', )

    #search_fields = ['pk', 'title', 'text']
