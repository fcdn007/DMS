from django.urls import path

from . import views

app_name = "LIMS"
urlpatterns = [
    path('Methy/MethyLibraryInfo/', views.MethyLibraryInfoV, name='MethyLibraryInfo'),
    path('Methy/MethyCaptureInfo/', views.MethyCaptureInfoV, name='MethyCaptureInfo'),
    path('Methy/MethyPoolingInfo/', views.MethyPoolingInfoV, name='MethyPoolingInfo')
]