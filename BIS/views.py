from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets

from util.utils import get_queryset_base, singleModelV
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
    col_name = ["华大编号", "血浆管数", "癌组织样本数量", "癌旁组织样本数量", "白细胞样本数量", "粪便样本数量", "备注",
                "上次修改时间", "创建时间"]
    return singleModelV(request, 0, 'BIS/SampleInventoryInfo.html', col_name)


@login_required
@permission_required('BIS.view_sampleinfo')
def SampleInfoV(request):
    col_name = ["生物样本编号", "华大编号", "原始样本编号", "冰箱位置", "孔板号", "孔位", "样本类型", "采样日期", "寄送日期",
                "备注", "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo']
    return singleModelV(request, 1, 'BIS/SampleInfo.html', col_name, drop_cols=drop_cols)


@login_required
@permission_required('BIS.view_extractinfo')
def ExtractInfoV(request):
    col_name = ["核酸提取编号", "华大编号", "生物样本编号", "提取日期", "样本类型", "核酸类型", "样本体积(ml)/质量(mg)",
                "提取方法", "浓度(ng/ul)", "体积(ul)", "冰箱位置", "孔板号", "孔位", "提取总量(ng)", "成功建库使用量(ng)",
                "失败建库使用量(ng)", "科研项目使用量(ng)", "其他使用量(ng)", "剩余量(ng)", "备注", "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo', 'sampleinfo']
    return singleModelV(request, 2, 'BIS/ExtractInfo.html', col_name, drop_cols=drop_cols)


@login_required
@permission_required('BIS.view_dnausagerecordinfo')
def DNAUsageRecordInfoV(request):
    col_name = ["核酸提取编号", "华大编号", "使用日期", "使用量(ng)", "用途", "建库编号(如有)", "备注", "上次修改时间", "创建时间"]
    drop_cols=['sampleinventoryinfo', 'extractinfo']
    return singleModelV(request, 3, 'BIS/DNAUsageRecordInfo.html', col_name, drop_cols=drop_cols)
