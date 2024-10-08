from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib


class KareliahistoryResource(resources.ModelResource):
    class Meta:
        model = Kareliahistory
        
#class NoteAdmin(ImportExportActionModelAdmin):
    #resource_class = ProductResource
    #list_display = ('pk', 'text',)
book_resource = resources.modelresource_factory(model=Kareliahistory)()
dataset = tablib.Dataset(['', 'New book'], headers=['id', 'title'])
result = book_resource.import_data(dataset, dry_run=True)
print(result.has_errors())
False
result = book_resource.import_data(dataset, dry_run=False)


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
