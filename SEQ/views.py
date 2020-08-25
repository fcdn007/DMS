from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import F
from rest_framework import viewsets

from util.utils import get_queryset_base, singleModelV
from .serializers import *


# Create your views here.
class SequencingInfoViewSet(viewsets.ModelViewSet):
    queryset = SequencingInfo.objects.all()
    serializer_class = SequencingInfoSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset_raw = get_queryset_base(SequencingInfo, self.request.query_params)
        return queryset_raw.annotate(poolingLB_id=F('methycaptureinfo__poolingLB_id'))


class MethyQCInfoViewSet(viewsets.ModelViewSet):
    queryset = MethyQCInfo.objects.all()
    serializer_class = MethyQCInfoSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset_raw = get_queryset_base(MethyQCInfo, self.request.query_params)
        return queryset_raw.annotate(sampler_id=F('sampleinventoryinfo__sampler_id'),
                                     singleLB_Pooling_id=F('methypoolinginfo__singleLB_Pooling_id'),
                                     sequencing_id=F('sequencinginfo__sequencing_id'))


@login_required
@permission_required('SEQ.view_sequencinginfo')
def SequencingInfoV(request):
    col_name = ["上机文库号", "捕获文库名", "送测日期", "上机时间", "下机时间", "机器号", "芯片号", "备注", "上次修改时间",
                "创建时间"]
    drop_cols = ['methycaptureinfo']
    return singleModelV(request, 7, 'SEQ/SequencingInfo.html', col_name, drop_cols=drop_cols)


@login_required
@permission_required('SEQ.view_methyqcinfo')
def MethyQCInfoV(request):
    col_name = ["Sample", "Data_Size(Gb)", "Clean_Rate(%)", "R1_Q20", "R2_Q20", "R1_Q30", "R2_Q30",
                "GC_Content", "BS_conversion_rate(lambda_DNA)", "BS_conversion_rate(CHH)",
                "BS_conversion_rate(CHG)", "Uniquely_Paired_Mapping_Rate", "Mismatch_and_InDel_Rate",
                "Mode_Fragment_Length(bp)", "Genome_Duplication_Rate", "Genome_Depth(X)",
                "Genome_Dedupped_Depth(X)", "Genome_Coverage", "Genome_4X_CpG_Depth(X)", "Genome_4X_CpG_Coverage",
                "Genome_4X_CpG_methylation_level", "Panel_4X_CpG_Depth(X)", "Panel_4X_CpG_Coverage",
                "Panel_4X_CpG_methylation_level", "Panel_Ontarget_Rate(region)", "Panel_Duplication_Rate(region)",
                "Panel_Depth(site,X)", "Panel_Dedupped_Depth(site,X)", "Panel_Coverage(site,1X)",
                "Panel_Coverage(site,10X)", "Panel_Coverage(site,20X)", "Panel_Coverage(site,50X)",
                "Panel_Coverage(site,100X)", "Panel_Uniformity(site,>20%mean)", "Strand_balance(F)",
                "Strand_balance(R)", "GC_bin_depth_ratio", "华大编号", "测序文库编号", "上机文库号", "备注",
                "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo', 'methypoolinginfo', 'sequencinginfo']
    return singleModelV(request, 8, 'SEQ/MethyQCInfo.html', col_name, drop_cols=drop_cols)
