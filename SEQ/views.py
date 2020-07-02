from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required, permission_required

from util.utils import get_queryset_base
from .serializers import *


# Create your views here.
class SequencingInfoViewSet(viewsets.ModelViewSet):
    queryset = SequencingInfo.objects.all()
    serializer_class = SequencingInfoSerializer

    def get_queryset(self):
        return get_queryset_base(SequencingInfo, self.request.query_params)


class MethyQCInfoViewSet(viewsets.ModelViewSet):
    queryset = MethyQCInfo.objects.all()
    serializer_class = MethyQCInfoSerializer

    def get_queryset(self):
        return get_queryset_base(MethyQCInfo, self.request.query_params)


@login_required
@permission_required('SEQ.view_sequencinginfo')
def SequencingInfoV(request):
    return render(request, 'SEQ/SequencingInfo.html')


@login_required
@permission_required('SEQ.view_methyqcinfo')
def MethyQCInfoV(request):
    return render(request, 'SEQ/MethyQCInfo.html')


