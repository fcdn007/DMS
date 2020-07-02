from django.conf import settings
from rest_framework import serializers

from .models import SampleInventoryInfo, SampleInfo, ExtractInfo, DNAUsageRecordInfo
from util.serializers import DynamicFieldsModelSerializer


class SampleInventoryInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = SampleInventoryInfo
        fields = ('sampler_id', 'plasma_num', 'adjacent_mucosa_num', 'cancer_tissue_num', 'WBC_num', 'stool_num', 'memo',
                  'index', 'last_modify_time', 'create_time')


class SampleInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = SampleInfo
        fields = ('sample_id', 'sampler_id', 'raw_id', 'fridge', 'plate', 'well', 'sample_type', 'memo', 'index',
                  'last_modify_time', 'create_time')


class ExtractInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    totalM = serializers.SerializerMethodField()
    remainM = serializers.SerializerMethodField()

    def get_totalM(self, obj):
        return round(obj.dna_con * obj.dna_vol, 3)

    def get_remainM(self, obj):
        return round(obj.dna_con*obj.dna_vol-obj.successM-obj.failM-obj.researchM-obj.othersM, 3)

    class Meta:
        model = ExtractInfo
        fields = ('dna_id', 'sampler_id', 'sample_id', 'extract_date', 'sample_type', 'nucleic_type', 'sample_volume',
                  'extract_method', 'dna_con', 'dna_vol', 'fridge', 'plate', 'well', 'totalM', 'successM', 'failM',
                  'researchM', 'othersM', 'remainM', 'memo', 'index', 'last_modify_time', 'create_time')


class DNAUsageRecordInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = DNAUsageRecordInfo
        fields = ('dna_id', 'sampler_id', 'sample_id', 'usage_date', 'mass', 'usage', 'singleLB_id', 'memo', 'index',
                  'last_modify_time', 'create_time')
