from django.conf import settings
from rest_framework import serializers

from .models import MethyLibraryInfo, MethyCaptureInfo, MethyPoolingInfo
from util.serializers import DynamicFieldsModelSerializer


class MethyLibraryInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    dnaCon = serializers.SerializerMethodField()

    def get_dnaCon(self, obj):
        return f"{obj.dna_id.dna_con}"

    class Meta:
        model = MethyLibraryInfo
        fields = ('singleLB_id', 'sampler_id', 'sample_id', 'dna_id', 'tube_id', 'clinical_boolen', 'singleLB_name',
                  'label', 'barcodes', 'LB_date', 'LB_method', 'kit_batch', 'dnaCon', 'mass', 'pcr_cycles', 'LB_con',
                  'LB_vol', 'operator', 'memo', 'index', 'last_modify_time', 'create_time')


class MethyCaptureInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = MethyCaptureInfo
        fields = ('poolingLB_id', 'hybrid_date', 'probes', 'hybrid_min', 'postpcr_cycles', 'postpcr_con', 'elution_vol',
                  'operator', 'memo', 'index', 'last_modify_time', 'create_time')


class MethyPoolingInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = MethyPoolingInfo
        fields = ('sampler_id', 'sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'pooling_ratio', 'mass', 'volume',
                  'singleLB_Pooling_id', 'memo', 'index', 'last_modify_time', 'create_time')
