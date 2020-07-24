from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from rest_framework import viewsets

from databaseDemo.tasks import add_modelViewRecord_by_celery
from util.utils import get_queryset_base, output_model_all_records
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
    output_all_bool = request.GET.get('all', 0)
    if output_all_bool:
        serializer = MethyLibraryInfoSerializer(MethyLibraryInfo.objects.all(), many=True)
        col_name = ["建库编号", "华大编号", "核酸提取编号", "管上编号", "是否临床", "样本标签", "文库名", "index列表", "建库日期",
                    "建库方法", "试剂批次", "核酸样本浓度(ug/ul)", "起始量(ng)", "PCR循环数", "文库浓度(ng/ul)", "文库体积(ul)",
                    "操作人", "备注", "上次修改时间", "创建时间"]
        return output_model_all_records("MethyLibraryInfo", serializer.data, col_name,
                                        drop_cols=['sampleinventoryinfo', 'extractinfo'])
    else:
        return render(request, 'LIMS/MethyLibraryInfo.html')


@login_required
@permission_required('LIMS.view_methycaptureinfo')
def MethyCaptureInfoV(request):
    add_modelViewRecord_by_celery("MethyCaptureInfo", request.user.username)
    output_all_bool = request.GET.get('all', 0)
    if output_all_bool:
        serializer = MethyCaptureInfoSerializer(MethyCaptureInfo.objects.all(), many=True)
        col_name = ["捕获文库名", "杂交日期", "杂交探针", "杂交时间(min)", "PostPCR循环数", "PostPCR浓度(ng/ul)",
                    "洗脱体积(ul)", "操作人", "备注", "上次修改时间", "创建时间"]
        return output_model_all_records("MethyCaptureInfo", serializer.data, col_name)
    else:
        return render(request, 'LIMS/MethyCaptureInfo.html')


@login_required
@permission_required('LIMS.view_methypoolinginfo')
def MethyPoolingInfoV(request):
    add_modelViewRecord_by_celery("MethyPoolingInfo", request.user.username)
    output_all_bool = request.GET.get('all', 0)
    if output_all_bool:
        serializer = MethyPoolingInfoSerializer(MethyPoolingInfo.objects.all(), many=True)
        col_name = ["建库编号", "捕获文库名", "测序文库编号", "华大编号", "pooling比例", "取样(ng)", "体积(ul)", "备注",
                    "上次修改时间", "创建时间"]
        return output_model_all_records("MethyPoolingInfo", serializer.data, col_name,
                                        drop_cols=['sampleinventoryinfo', 'methylibraryinfo', 'methycaptureinfo'])
    else:
        return render(request, 'LIMS/MethyPoolingInfo.html')

