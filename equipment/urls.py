from django.urls import path
from . import views

urlpatterns = [
    path('measureequipmentall/', views.MeasurEquipmentView.as_view(), name='measureequipmentall'),
    path('measureequipmentallsearres/', views.SearchResultMeasurEquipmentView.as_view(), name='measureequipmentallsearres'),
    path('measureequipmentstr/<int:pk>/', views.StrMeasurEquipmentView.as_view(), name='measureequipmentstr' + 'pk'),
    # path(r'^export/xls/$', views.export_me_xls, name='export_me_xls'),
]
