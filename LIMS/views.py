from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import F
from rest_framework import viewsets

from util.utils import get_queryset_base, singleModelV
from .serializers import *


# Create your views here.
class MethyLibraryInfoViewSet(viewsets.ModelViewSet):
    queryset = MethyLibraryInfo.objects.all()
    serializer_class = MethyLibraryInfoSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset_raw = get_queryset_base(MethyLibraryInfo, self.request.query_params)
        return queryset_raw.annotate(sampler_id=F('sampleinventoryinfo__sampler_id'), dna_id=F('extractinfo__dna_id'),
                                     dna_con=F('extractinfo__dna_con'))


class MethyCaptureInfoViewSet(viewsets.ModelViewSet):
    queryset = MethyCaptureInfo.objects.all()
    serializer_class = MethyCaptureInfoSerializer

    def get_queryset(self):
        return get_queryset_base(MethyCaptureInfo, self.request.query_params)



class MethyPoolingInfoViewSet(viewsets.ModelViewSet):
    queryset = MethyPoolingInfo.objects.all()
    serializer_class = MethyPoolingInfoSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset_raw = get_queryset_base(MethyPoolingInfo, self.request.query_params)
        return queryset_raw.annotate(sampler_id=F('sampleinventoryinfo__sampler_id'),
                                     singleLB_id=F('methylibraryinfo__singleLB_id'),
                                     poolingLB_id=F('methycaptureinfo__poolingLB_id'))


@login_required
@permission_required('LIMS.view_methylibraryinfo')
def MethyLibraryInfoV(request):
    col_name = ["建库编号", "华大编号", "核酸提取编号", "管上编号", "是否临床", "样本标签", "文库名", "index列表", "建库日期",
                "建库方法", "试剂批次", "核酸样本浓度(ug/ul)", "起始量(ng)", "PCR循环数", "文库浓度(ng/ul)", "文库体积(ul)",
                "操作人", "备注", "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo', 'extractinfo']
    return singleModelV(request, 4, 'LIMS/MethyLibraryInfo.html', col_name, drop_cols=drop_cols)


@login_required
@permission_required('LIMS.view_methycaptureinfo')
def MethyCaptureInfoV(request):
    col_name = ["捕获文库名", "杂交日期", "杂交探针", "杂交时间(min)", "PostPCR循环数", "PostPCR浓度(ng/ul)",
                "洗脱体积(ul)", "操作人", "备注", "上次修改时间", "创建时间"]
    return singleModelV(request, 5, 'LIMS/MethyCaptureInfo.html', col_name)


@login_required
@permission_required('LIMS.view_methypoolinginfo')
def MethyPoolingInfoV(request):
    col_name = ["建库编号", "捕获文库名", "测序文库编号", "华大编号", "pooling比例", "取样(ng)", "体积(ul)", "备注",
                "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo', 'methylibraryinfo', 'methycaptureinfo']
    return singleModelV(request, 6, 'LIMS/MethyPoolingInfo.html', col_name, drop_cols=drop_cols)

