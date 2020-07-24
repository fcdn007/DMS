from django.urls import path

from . import views

app_name = "EMR"
urlpatterns = [
    path('ClinicalInfo/', views.ClinicalInfoV, name='ClinicalInfo'),
    path('FollowupInfo/', views.FollowupInfoV, name='FollowupInfo'),
    path('Pathology/LiverPathologicalInfo/', views.LiverPathologicalInfoV, name='LiverPathologicalInfo'),
    path('Test/TMDInfo/', views.TMDInfoV, name='TMDInfo'),
    path('Test/BiochemInfo/', views.BiochemInfoV, name='BiochemInfo')
]