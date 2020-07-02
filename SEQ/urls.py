from django.urls import path
from . import views


app_name = "SEQ"
urlpatterns = [
    path('SequencingInfo/', views.SequencingInfoV, name='SequencingInfo'),
    path('MethyQCInfo/', views.MethyQCInfoV, name='MethyQCInfo')
]