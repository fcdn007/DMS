from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required, permission_required

from util.utils import get_queryset_base
from .serializers import *


# Create your views here.
class SampleInventoryInfoViewSet(viewsets.ModelViewSet):
    queryset = SampleInventoryInfo.objects.all()
    serializer_class = SampleInventoryInfoSerializer

    def get_queryset(self):
        return get_queryset_base(SampleInventoryInfo, self.request.query_params)


class SampleInfoViewSet(viewsets.ModelViewSet):
    queryset = SampleInfo.objects.all()
    serializer_class = SampleInfoSerializer

    def get_queryset(self):
        return get_queryset_base(SampleInfo, self.request.query_params)


class ExtractInfoViewSet(viewsets.ModelViewSet):
    queryset = ExtractInfo.objects.all()
    serializer_class = ExtractInfoSerializer

    def get_queryset(self):
        return get_queryset_base(ExtractInfo, self.request.query_params)


class DNAUsageRecordInfoViewSet(viewsets.ModelViewSet):
    queryset = DNAUsageRecordInfo.objects.all()
    serializer_class = DNAUsageRecordInfoSerializer

    def get_queryset(self):
        return get_queryset_base(DNAUsageRecordInfo, self.request.query_params)


@login_required
@permission_required('BIS.view_sampleinventoryinfo')
def SampleInventoryInfoV(request):
    return render(request, 'BIS/SampleInventoryInfo.html')


@login_required
@permission_required('BIS.view_sampleinfo')
def SampleInfoV(request):
    return render(request, 'BIS/SampleInfo.html')


@login_required
@permission_required('BIS.view_extractinfo')
def ExtractInfoV(request):
    return render(request, 'BIS/ExtractInfo.html')


@login_required
@permission_required('BIS.view_dnausagerecordinfo')
def DNAUsageRecordInfoV(request):
    return render(request, 'BIS/DNAUsageRecordInfo.html')
