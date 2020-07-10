from django.urls import path

from . import views

app_name = "EMR"
urlpatterns = [
    path('ClinicalInfo/', views.ClinicalInfoV, name='ClinicalInfo'),
    path('FollowupInfo/', views.FollowupInfoV, name='FollowupInfo'),
    path('LiverPathologicalInfo/', views.LiverPathologicalInfoV, name='LiverPathologicalInfo'),
    path('TMDInfo/', views.TMDInfoV, name='TMDInfo'),
    path('BiochemInfo/', views.BiochemInfoV, name='BiochemInfo')
]