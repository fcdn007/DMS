from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from rest_framework import viewsets

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
    return render(request, 'EMR/ClinicalInfo.html')


@login_required
@permission_required('EMR.view_followupinfo')
def FollowupInfoV(request):
    return render(request, 'EMR/FollowupInfo.html')


@login_required
@permission_required('EMR.view_liverpathologicalinfo')
def LiverPathologicalInfoV(request):
    return render(request, 'EMR/LiverPathologicalInfo.html')


@login_required
@permission_required('EMR.view_tmdinfo')
def TMDInfoV(request):
    return render(request, 'EMR/TMDInfo.html')


@login_required
@permission_required('EMR.view_biocheminfo')
def BiochemInfoV(request):
    return render(request, 'EMR/BiochemInfo.html')

