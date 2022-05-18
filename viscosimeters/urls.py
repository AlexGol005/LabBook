from django.urls import path, include
from . import views

urlpatterns = [
    path('viscosimetersType/', views.ViscosimeterTypeView.as_view(), name='viscosimetersType'),
    path('viscosimetersKonstants/', views.ViscosimetersKonstantsView.as_view(), name='viscosimetersKonstants'),
]

# path('viscosimeters/', views.ViscosimeterTypeView.as_view(), name='vt'),
