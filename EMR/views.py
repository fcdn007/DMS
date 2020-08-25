from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import F
from rest_framework import viewsets

from util.utils import get_queryset_base, singleModelV
from .serializers import *


# Create your views here.
class ClinicalInfoViewSet(viewsets.ModelViewSet):
    queryset = ClinicalInfo.objects.all()
    serializer_class = ClinicalInfoSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset_raw = get_queryset_base(ClinicalInfo, self.request.query_params)
        return queryset_raw.annotate(sampler_id=F('sampleinventoryinfo__sampler_id'))


class FollowupInfoViewSet(viewsets.ModelViewSet):
    queryset = FollowupInfo.objects.all()
    serializer_class = FollowupInfoSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset_raw = get_queryset_base(FollowupInfo, self.request.query_params)
        return queryset_raw.annotate(sampler_id=F('sampleinventoryinfo__sampler_id'),
                                     clinical_id=F('clinicalinfo__clinical_id'))


class LiverPathologicalInfoViewSet(viewsets.ModelViewSet):
    queryset = LiverPathologicalInfo.objects.all()
    serializer_class = LiverPathologicalInfoSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset_raw = get_queryset_base(LiverPathologicalInfo, self.request.query_params)
        return queryset_raw.annotate(sampler_id=F('sampleinventoryinfo__sampler_id'),
                                     clinical_id=F('clinicalinfo__clinical_id'))


class TMDInfoViewSet(viewsets.ModelViewSet):
    queryset = TMDInfo.objects.all()
    serializer_class = TMDInfoSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset_raw = get_queryset_base(TMDInfo, self.request.query_params)
        return queryset_raw.annotate(sampler_id=F('sampleinventoryinfo__sampler_id'),
                                     clinical_id=F('clinicalinfo__clinical_id'))



class BiochemInfoViewSet(viewsets.ModelViewSet):
    queryset = BiochemInfo.objects.all()
    serializer_class = BiochemInfoSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset_raw = get_queryset_base(BiochemInfo, self.request.query_params)
        return queryset_raw.annotate(sampler_id=F('sampleinventoryinfo__sampler_id'),
                                     clinical_id=F('clinicalinfo__clinical_id'))


@login_required
@permission_required('EMR.view_clinicalinfo')
def ClinicalInfoV(request):
    col_name = ["病历编号", "华大编号", "住院号", "医院编号", "科室", "姓名", "性别", "年龄", "记录日期", "肿瘤类型",
                "分化程度", "肿瘤最大径", "TNM分期", "AJCC分期", "备注", "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo']
    return singleModelV(request, 9, 'EMR/ClinicalInfo.html', col_name, drop_cols=drop_cols)


@login_required
@permission_required('EMR.view_followupinfo')
def FollowupInfoV(request):
    col_name = ["病历编号", "华大编号", "生存状态", "死亡日期", "死因是否与肿瘤相关", "死亡原因", "是否复发", "复发日期", "复发状态",
                "复发转移部位", "随访日期", "随访情况", "备注", "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo', 'clinicalinfo']
    return singleModelV(request, 10, 'EMR/FollowupInfo.html', col_name, drop_cols=drop_cols)


@login_required
@permission_required('EMR.view_liverpathologicalinfo')
def LiverPathologicalInfoV(request):
    col_name = ["病理报告编号", "病历编号", "华大编号", "检查日期", "检查阶段", "病理类型", "分化程度", "肿瘤数目", "肿瘤最大径",
                "肿瘤2直径", "肿瘤3直径", "肝包膜侵犯(肝被膜)", "淋巴结转移", "淋巴结转移类型", "肉眼癌栓(脉管侵犯)", "微血管浸润",
                "MVI风险等级", "切面距癌距离(切除面)", "G评分", "S评分", "备注", "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo', 'clinicalinfo']
    return singleModelV(request, 11, 'EMR/LiverPathologicalInfo.html', col_name, drop_cols=drop_cols)


@login_required
@permission_required('EMR.view_tmdinfo')
def TMDInfoV(request):
    col_name = ["病历编号", "华大编号", "检查日期", "检查阶段", "甲胎蛋白", "甲胎蛋白异质体", "癌胚抗原", "糖类抗原19-9",
                "黑素瘤抑制蛋白", "细胞角蛋白19片段", "糖类抗原125", "神经元特异性烯醇化酶", "鳞状细胞癌抗原", "胃泌素释放肽前体",
                "糖类抗原15-3", "前列腺特异性抗原", "备注", "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo', 'clinicalinfo']
    return singleModelV(request, 12, 'EMR/TMDInfo.html', col_name, drop_cols=drop_cols)


@login_required
@permission_required('EMR.view_biocheminfo')
def BiochemInfoV(request):
    col_name = ["病历编号", "华大编号", "检查日期", "检查阶段", "总胆红素", "丙氨酸氨基转移酶", "γ-谷氨酰转移酶", "白蛋白",
                "α-L-岩藻糖苷酶", "直接胆红素", "谷丙转氨酶", "谷草转氨酶", "r-谷氨酰转肽酶", "碱性磷酸酶", "总胆汁酸",
                "前白蛋白", "备注", "上次修改时间", "创建时间"]
    drop_cols = ['sampleinventoryinfo', 'clinicalinfo']
    return singleModelV(request, 13, 'EMR/BiochemInfo.html', col_name, drop_cols=drop_cols)

