from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from rest_framework import viewsets

from databaseDemo.tasks import add_modelViewRecord_by_celery
from util.utils import get_queryset_base
from .serializers import *


# Create your views here.
class MethyLibraryInfoViewSet(viewsets.ModelViewSet):
    queryset = MethyLibraryInfo.objects.all()
    serializer_class = MethyLibraryInfoSerializer

    def get_queryset(self):
        return get_queryset_base(MethyLibraryInfo, self.request.query_params)


class MethyCaptureInfoViewSet(viewsets.ModelViewSet):
    queryset = MethyCaptureInfo.objects.all()
    serializer_class = MethyCaptureInfoSerializer

    def get_queryset(self):
        return get_queryset_base(MethyCaptureInfo, self.request.query_params)


class MethyPoolingInfoViewSet(viewsets.ModelViewSet):
    queryset = MethyPoolingInfo.objects.all()
    serializer_class = MethyPoolingInfoSerializer

    def get_queryset(self):
        return get_queryset_base(MethyPoolingInfo, self.request.query_params)


@login_required
@permission_required('LIMS.view_methylibraryinfo')
def MethyLibraryInfoV(request):
    add_modelViewRecord_by_celery("MethyLibraryInfo", request.user.username)
    return render(request, 'LIMS/MethyLibraryInfo.html')


@login_required
@permission_required('LIMS.view_methycaptureinfo')
def MethyCaptureInfoV(request):
    add_modelViewRecord_by_celery("MethyCaptureInfo", request.user.username)
    return render(request, 'LIMS/MethyCaptureInfo.html')


@login_required
@permission_required('LIMS.view_methypoolinginfo')
def MethyPoolingInfoV(request):
    add_modelViewRecord_by_celery("MethyPoolingInfo", request.user.username)
    return render(request, 'LIMS/MethyPoolingInfo.html')

