from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required, permission_required

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


class LiverTMDInfoViewSet(viewsets.ModelViewSet):
    queryset = LiverTMDInfo.objects.all()
    serializer_class = LiverTMDInfoSerializer

    def get_queryset(self):
        return get_queryset_base(LiverTMDInfo, self.request.query_params)



class LiverBiochemInfoViewSet(viewsets.ModelViewSet):
    queryset = LiverBiochemInfo.objects.all()
    serializer_class = LiverBiochemInfoSerializer

    def get_queryset(self):
        return get_queryset_base(LiverBiochemInfo, self.request.query_params)


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
@permission_required('EMR.view_livertmdinfo')
def LiverTMDInfoV(request):
    return render(request, 'EMR/LiverTMDInfo.html')


@login_required
@permission_required('EMR.view_liverbiocheminfo')
def LiverBiochemInfoV(request):
    return render(request, 'EMR/LiverBiochemInfo.html')

