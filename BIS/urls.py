from django.urls import path
from . import views


app_name = "BIS"
urlpatterns = [
    path('SampleInventoryInfo/', views.SampleInventoryInfoV, name='SampleInventoryInfo'),
    path('SampleInfo/', views.SampleInfoV, name='SampleInfo'),
    path('ExtractInfo/', views.ExtractInfoV, name='ExtractInfo'),
    path('DNAUsageRecordInfo/', views.DNAUsageRecordInfoV, name='DNAUsageRecordInfo')
]
