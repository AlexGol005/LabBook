from django.urls import path
from . import views

urlpatterns = [
    path('measureequipmentall/', views.MeasurEquipmentView.as_view(), name='measureequipmentall'),
    path('measureequipmentall/mustver/', views.SearchMustVerView.as_view(), name='mustver'),
    path('measureequipmentall/notver/', views.SearchNotVerView.as_view(), name='notver'),
    path('measureequipmentall/mustorder/', views.SearchMustOrderView.as_view(), name='mustorder'),
    path('testingequipmentall/', views.TestingEquipmentView.as_view(), name='testingequipmentall'),
    path('measureequipmentallsearres/', views.SearchResultMeasurEquipmentView.as_view(), name='measureequipmentallsearres'),
    path('testingequipmentallsearres/', views.SearchResultTestingEquipmentView.as_view(), name='testingequipmentallsearres'),
    path('measureequipment/<str:str>/', views.StrMeasurEquipmentView.as_view(), name='measureequipment'),
    path('testequipment/<str:str>/', views.StrTestEquipmentView.as_view(), name='testequipment'),
    path(r'^export/xls/$', views.export_me_xls, name='export_me_xls'),
    path(r'^export3/xls/$', views.export_mustver_xls, name='export_mustver_xls'),
    path('measureequipment/<str:str>/comments/', views.CommentsView.as_view(), name='measureequipmentcomm'),
    path('measureequipment/<str:str>/metrologyindividuality/', views.EquipmentMetrologyUpdate, name='metrologyindividuality'),
    path('measureequipment/<str:str>/individuality/', views.EquipmentUpdate, name='measureequipmentind'),
    path('measureequipment/verification/<str:str>/', views.VerificationequipmentView.as_view(), name='measureequipmentver'),
    path('testingequipment/attestation/<str:str>/', views.AttestationequipmentView.as_view(), name='testingequipmentatt'),
    path('measureequipment/verificationreg/<str:str>/', views.VerificationReg, name='measureequipmentverificationreg'),
    path('testingequipment/attestationreg/<str:str>/', views.AttestationReg, name='testingequipmentattestationreg'),
    path('equipmentreg/', views.EquipmentReg, name='equipmentreg'),
    path('equipmentlist/', views.EquipmentView.as_view(), name='equipmentlist'),
    path('manufacturerlist/', views.ManufacturerView.as_view(), name='manufacturerlist'),
    path('manufacturerreg/', views.ManufacturerRegView.as_view(), name='manufacturerreg'),
    path('measurequipmentcharacterslist/', views.MeasurEquipmentCharaktersView.as_view(), name='measurequipmentcharacterslist'),
    path('testingequipmentcharacterslist/', views.TestingEquipmentCharaktersView.as_view(), name='testingequipmentcharacterslist'),
    path('measurequipmentcharactersreg/', views.MeasurEquipmentCharaktersRegView.as_view(), name='measurequipmentcharactersreg'),
    path('measurequipmentcharactersupdate/<str:str>/', views.MeasurEquipmentCharaktersUpdateView, name='measurequipmentcharactersupdate'),
    path('testequipmentcharactersupdate/<str:str>/', views.TestingEquipmentCharaktersUpdateView, name='testequipmentcharactersupdate'),
    path('testingequipmentcharactersreg/', views.TestingEquipmentCharaktersRegView.as_view(), name='testingequipmentcharactersreg'),
    path('measureequipmentreg/<str:str>/', views.MeasureequipmentregView.as_view(), name='measureequipmentreg'),
    path('testequipmentreg/<str:str>/', views.TestingequipmentregView.as_view(), name='testequipmentreg'),
    path('helpequipmentreg/<str:str>/', views.HelpingequipmentregView.as_view(), name='helpequipmentreg'),
    path('personchangereg/<str:str>/', views.PersonchangeFormView.as_view(), name='personchangereg'),
    path('roomschangereg/<str:str>/', views.RoomschangeFormView.as_view(), name='roomschangereg'),
    path('meteo/', views.MeteorologicalParametersView.as_view(), name='meteo'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('roomreg/', views.RoomsCreateView.as_view(), name='roomreg'),
    path('meteoreg/', views.MeteorologicalParametersCreateView.as_view(), name='meteoreg'),
    path('docsreg/<str:str>/', views.DocsConsView.as_view(), name='docsreg'),
    path('verificators/', views.VerificatorsView.as_view(), name='verificators'),
    path('verificatorsreg/', views.VerificatorsCreationView.as_view(), name='verificatorsreg'),
    path('verificatorsupdate/<str:str>/', views.VerificatorUpdate, name='verificatorsupdate'),
    path('verificatorpersons/', views.VerificatorsPersonsView.as_view(), name='verificatorpersons'),
    path('verificatorspersonsreg/', views.VerificatorPersonCreationView.as_view(), name='verificatorspersonsreg'),
    path(r'^export1/xls/$/<int:pk>', views.export_mecard_xls, name='export_mecard_xls'),
    path(r'^export111/xls/$/<int:pk>', views.export_tecard_xls, name='export_tecard_xls'),
    path(r'^export10/xls/$/<int:pk>', views.export_exvercard_xls, name='export_exvercard_xls'),
    path(r'^export100/xls/$/<int:pk>', views.export_exvercardteste_xls, name='export_exvercardteste_xls'),
    path(r'^export2/xls/$/', views.export_verificlabel_xls, name='export_verificlabel_xls'),
    path('chromato/', views.ChromatoView.as_view(), name='chromato'),
    path('reestrsearres/', views.ReestrsearresView.as_view(), name='reestrsearres'),
    path('testingsearres/', views.TEcharacterssearresView.as_view(), name='testingsearres'),
    path('metro/', views.MetrologicalEnsuringView.as_view(), name='metro'),
    path('verificationlabels/', views.VerificationLabelsView.as_view(), name='verificationlabels'),
    path('contactsverreg/<str:str>/', views.ContactsVerregView.as_view(), name='contactsverreg'),
    path('haveorder/<int:pk>/', views.HaveorderVerView.as_view(), name='haveorder'),
    path('haveorderatt/<int:pk>/', views.HaveorderAttView.as_view(), name='haveorderatt'),
    path('lasttenequipment/', views.LastNewEquipmentView.as_view(), name='lasttenequipment'),
    path(r'^export70/xls/$', views.export_metroyear_xls, name='export_metroyear_xls'),
    path(r'^export71/xls/$', views.export_metroyearprice_xls, name='export_metroyearprice_xls'),
    path(r'^export72/xls/$', views.export_metroyearcust_xls, name='export_metroyearcust_xls'),
    path(r'^export73/xls/$', views.export_metronewyear_xls, name='export_metronewyear_xls'),
    path(r'^export74/xls/$', views.export_planmetro_xls, name='export_planmetro_xls'),
    path(r'^export75/xls/$', views.export_plan_purchaesing_xls, name='export_plan_purchaesing_xls'),
    path(r'^export80/xls/$', views.export_maintenance_schedule_xls, name='export_maintenance_schedule_xls'),
]
