from django.urls import path
from . import views

urlpatterns = [
    path('measureequipmentall/', views.MeasurEquipmentView.as_view(), name='measureequipmentall'),
    path('testingequipmentall/', views.TestingEquipmentView.as_view(), name='testingequipmentall'),
    path('measureequipmentallsearres/', views.SearchResultMeasurEquipmentView.as_view(), name='measureequipmentallsearres'),
    path('testingequipmentallsearres/', views.SearchResultTestingEquipmentView.as_view(), name='testingequipmentallsearres'),
    path('measureequipment/<str:str>/', views.StrMeasurEquipmentView.as_view(), name='measureequipment'),
    path(r'^export/xls/$', views.export_me_xls, name='export_me_xls'),
    path('measureequipment/<str:str>/comments/', views.CommentsView.as_view(), name='measureequipmentcomm'),
    path('measureequipment/<str:str>/individuality/', views.EquipmentUpdate, name='measureequipmentind'),
    path('measureequipment/verification/<str:str>/', views.VerificationequipmentView.as_view(), name='measureequipmentver'),
    path('measureequipment/verificationreg/<str:str>/', views.VerificationReg, name='measureequipmentverificationreg'),
    path('equipmentreg/', views.EquipmentReg, name='equipmentreg'),
    path('equipmentlist/', views.EquipmentView.as_view(), name='equipmentlist'),
    path('manufacturerlist/', views.ManufacturerView.as_view(), name='manufacturerlist'),
    path('manufacturerreg/', views.ManufacturerRegView.as_view(), name='manufacturerreg'),
    path('measurequipmentcharacterslist/', views.MeasurEquipmentCharaktersView.as_view(), name='measurequipmentcharacterslist'),
    path('measurequipmentcharactersreg/', views.MeasurEquipmentCharaktersRegView.as_view(), name='measurequipmentcharactersreg'),
    path('measureequipmentreg/<str:str>/', views.MeasureequipmentregView.as_view(), name='measureequipmentreg'),
    path('personchangereg/<str:str>/', views.PersonchangeFormView.as_view(), name='personchangereg'),
    path('roomschangereg/<str:str>/', views.RoomschangeFormView.as_view(), name='roomschangereg'),
    path('meteo/', views.MeteorologicalParametersView.as_view(), name='meteo'),
    path('roomreg/', views.RoomsCreateView.as_view(), name='roomreg'),
    path('meteoreg/', views.MeteorologicalParametersCreateView.as_view(), name='meteoreg'),
    path('docsreg/<str:str>/', views.DocsConsView.as_view(), name='docsreg'),
    path('verificators/', views.VerificatorsView.as_view(), name='verificators'),
    path('verificatorsreg/', views.VerificatorsCreationView.as_view(), name='verificatorsreg'),
    path('verificatorpersons/', views.VerificatorsPersonsView.as_view(), name='verificatorpersons'),
    path('verificatorspersonsreg/', views.VerificatorPersonCreationView.as_view(), name='verificatorspersonsreg'),
    path(r'^export1/xls/$/<int:pk>', views.export_mecard_xls, name='export_mecard_xls'),
    path('chromato/', views.ChromatoView.as_view(), name='chromato'),
    path('reestrsearres/', views.ReestrsearresView.as_view(), name='reestrsearres'),
]
