from django.urls import path, include, re_path
from . import views


app_name = "ADVANCE"
urlpatterns = [
    path('Unique/', views.uniqueV, name='unique'),
    path('Upload/', views.uploadV, name='upload'),
    re_path(r'^download_excel/(?P<model>.*)/$', views.Download_excel, name='Download_excel'),
    # path('AdvanceSearch/', views.AdvanceSearchV, name='AdvanceSearch'),
    path('AdvanceUpload/', views.AdvanceUploadV, name='AdvanceUpload'),
    # path('plot_data/', views.plot_dataV, name='plot_data')
]
