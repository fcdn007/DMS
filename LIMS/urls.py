from django.urls import path
from . import views


app_name = "LIMS"
urlpatterns = [
    path('MethyLibraryInfo/', views.MethyLibraryInfoV, name='MethyLibraryInfo'),
    path('MethyCaptureInfo/', views.MethyCaptureInfoV, name='MethyCaptureInfo'),
    path('MethyPoolingInfo/', views.MethyPoolingInfoV, name='MethyPoolingInfo')
]