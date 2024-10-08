from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('viscosimeters.urls')),
    path('attestationJ/kinematicviscosity/', include('kinematicviscosity.urls')),
    path('attestationJ/dinamicviscosity/', include('dinamicviscosity.urls')),
    path('', include('users.urls')),
    path('equipment/', include('equipment.urls')),
    path('CertifiedValueJ/', include('jouViscosity.urls')),
    path('^', include('django.contrib.auth.urls')),
    path('blog/', include('blog.urls')),
    path('bdanswers/', include('bdanswers.urls')),
    path('postbox/', include('contact_form.urls')),
    path('hike/', include('hike.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.TOOLBAR_DEBUG:
    import debug_toolbar

    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
