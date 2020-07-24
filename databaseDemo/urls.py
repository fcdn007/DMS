"""databaseDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from BIS.views import SampleInventoryInfoViewSet, SampleInfoViewSet, ExtractInfoViewSet, DNAUsageRecordInfoViewSet
from EMR.views import BiochemInfoViewSet
from EMR.views import ClinicalInfoViewSet, FollowupInfoViewSet, LiverPathologicalInfoViewSet, TMDInfoViewSet
from LIMS.views import MethyLibraryInfoViewSet, MethyCaptureInfoViewSet, MethyPoolingInfoViewSet
from SEQ.views import SequencingInfoViewSet, MethyQCInfoViewSet
from USER.views import UserInfoViewSet, DatabaseRecordViewSet
from .views import HomeV, TestV, UrlSearchV

router = DefaultRouter()
router.register(r'BIS/SampleInventoryInfo', SampleInventoryInfoViewSet)
router.register(r'BIS/SampleInfo', SampleInfoViewSet)
router.register(r'BIS/ExtractInfo', ExtractInfoViewSet)
router.register(r'BIS/DNAUsageRecordInfo', DNAUsageRecordInfoViewSet)
router.register(r'EMR/ClinicalInfo', ClinicalInfoViewSet)
router.register(r'EMR/FollowupInfo', FollowupInfoViewSet)
router.register(r'EMR/Pathology/LiverPathologicalInfo', LiverPathologicalInfoViewSet)
router.register(r'EMR/Test/TMDInfo', TMDInfoViewSet)
router.register(r'EMR/Test/BiochemInfo', BiochemInfoViewSet)
router.register(r'LIMS/Methy/MethyLibraryInfo', MethyLibraryInfoViewSet)
router.register(r'LIMS/Methy/MethyCaptureInfo', MethyCaptureInfoViewSet)
router.register(r'LIMS/Methy/MethyPoolingInfo', MethyPoolingInfoViewSet)
router.register(r'SEQ/SequencingInfo', SequencingInfoViewSet)
router.register(r'SEQ/QC/MethyQCInfo', MethyQCInfoViewSet)
router.register(r'USER/UserInfo', UserInfoViewSet)
router.register(r'USER/DatabaseRecord', DatabaseRecordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('Home/', HomeV, name='Home'),
    path('BIS/', include('BIS.urls', namespace='BIS')),
    path('EMR/', include('EMR.urls', namespace='EMR')),
    path('LIMS/', include('LIMS.urls', namespace='LIMS')),
    path('SEQ/', include('SEQ.urls', namespace='SEQ')),
    path('USER/', include('USER.urls', namespace='USER')),
    path('ADVANCE/', include('ADVANCE.urls', namespace='ADVANCE')),
    # for rest_framework
    path('api/', include(router.urls)),
    re_path(r'Test/(?P<id>.*)/$', TestV, name='Test'),
    path('UrlSearch/', UrlSearchV, name='UrlSearch'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Added at 20170428 开发环境下，如果注释掉，无法正确加载静态文件
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
