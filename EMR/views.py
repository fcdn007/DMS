from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from rest_framework import viewsets

from databaseDemo.tasks import add_modelViewRecord_by_celery
from util.utils import get_queryset_base
from .serializers import *


# Create your views here.
class ClinicalInfoViewSet(viewsets.ModelViewSet):
    queryset = ClinicalInfo.objects.all()
    serializer_class = ClinicalInfoSerializer

    def get_queryset(self):
        return get_queryset_base(ClinicalInfo, self.request.query_params)


class FollowupInfoViewSet(viewsets.ModelViewSet):
    queryset = FollowupInfo.objects.all()
    serializer_class = FollowupInfoSerializer

    def get_queryset(self):
        return get_queryset_base(FollowupInfo, self.request.query_params)


class LiverPathologicalInfoViewSet(viewsets.ModelViewSet):
    queryset = LiverPathologicalInfo.objects.all()
    serializer_class = LiverPathologicalInfoSerializer

    def get_queryset(self):
        return get_queryset_base(LiverPathologicalInfo, self.request.query_params)


class TMDInfoViewSet(viewsets.ModelViewSet):
    queryset = TMDInfo.objects.all()
    serializer_class = TMDInfoSerializer

    def get_queryset(self):
        return get_queryset_base(TMDInfo, self.request.query_params)



class BiochemInfoViewSet(viewsets.ModelViewSet):
    queryset = BiochemInfo.objects.all()
    serializer_class = BiochemInfoSerializer

    def get_queryset(self):
        return get_queryset_base(BiochemInfo, self.request.query_params)


@login_required
@permission_required('EMR.view_clinicalinfo')
def ClinicalInfoV(request):
    add_modelViewRecord_by_celery("ClinicalInfo", request.user.username)
    return render(request, 'EMR/ClinicalInfo.html')


@login_required
@permission_required('EMR.view_followupinfo')
def FollowupInfoV(request):
    add_modelViewRecord_by_celery("FollowupInfo", request.user.username)
    return render(request, 'EMR/FollowupInfo.html')


@login_required
@permission_required('EMR.view_liverpathologicalinfo')
def LiverPathologicalInfoV(request):
    add_modelViewRecord_by_celery("LiverPathologicalInfo", request.user.username)
    return render(request, 'EMR/LiverPathologicalInfo.html')


@login_required
@permission_required('EMR.view_tmdinfo')
def TMDInfoV(request):
    add_modelViewRecord_by_celery("TMDInfo", request.user.username)
    return render(request, 'EMR/TMDInfo.html')


@login_required
@permission_required('EMR.view_biocheminfo')
def BiochemInfoV(request):
    add_modelViewRecord_by_celery("BiochemInfo", request.user.username)
    return render(request, 'EMR/BiochemInfo.html')

