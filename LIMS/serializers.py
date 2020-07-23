from django.conf import settings
from rest_framework import serializers

from util.serializers import DynamicFieldsModelSerializer
from .models import MethyLibraryInfo, MethyCaptureInfo, MethyPoolingInfo


class MethyLibraryInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    sampler_id = serializers.CharField(source='sampleinventoryinfo.sampler_id', read_only=True)
    dna_id = serializers.CharField(source='extractinfo.dna_id', read_only=True)
    dna_con = serializers.CharField(source='extractinfo.dna_con', read_only=True)

    class Meta:
        model = MethyLibraryInfo
        fields = ('singleLB_id', 'sampler_id', 'dna_id', 'tube_id', 'clinical_boolen', 'singleLB_name', 'label',
                  'barcodes', 'LB_date', 'LB_method', 'kit_batch', 'dna_con', 'mass', 'pcr_cycles', 'LB_con', 'LB_vol',
                  'operator', 'memo', 'id', 'last_modify_time', 'create_time', 'sampleinventoryinfo', 'extractinfo')


class MethyCaptureInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = MethyCaptureInfo
        fields = ('poolingLB_id', 'hybrid_date', 'probes', 'hybrid_min', 'postpcr_cycles', 'postpcr_con', 'elution_vol',
                  'operator', 'memo', 'id', 'last_modify_time', 'create_time')


class MethyPoolingInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    sampler_id = serializers.CharField(source='sampleinventoryinfo.sampler_id', read_only=True)
    singleLB_id = serializers.CharField(source='methylibraryinfo.singleLB_id', read_only=True)
    poolingLB_id = serializers.CharField(source='methycaptureinfo.poolingLB_id', read_only=True)

    class Meta:
        model = MethyPoolingInfo
        fields = ('sampler_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id', 'pooling_ratio', 'mass', 'volume',
                  'memo', 'id', 'last_modify_time', 'create_time', 'sampleinventoryinfo', 'methylibraryinfo',
                  'methycaptureinfo')
