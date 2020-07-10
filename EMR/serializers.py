from django.conf import settings
from rest_framework import serializers

from util.serializers import DynamicFieldsModelSerializer
from .models import ClinicalInfo, FollowupInfo, LiverPathologicalInfo, TMDInfo, BiochemInfo


class ClinicalInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    sampler_id = serializers.CharField(source='sampleinventoryinfo.sampler_id', read_only=True)

    class Meta:
        model = ClinicalInfo
        fields = ('clinical_id', 'sampler_id', 'patientId', 'hospital', 'department', 'name', 'gender', 'age',
                  'record_date', 'category', 'stage', 'tumor1_diam', 'memo', 'id', 'last_modify_time', 'create_time',
                  'sampleinventoryinfo')


class FollowupInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    sampler_id = serializers.CharField(source='sampleinventoryinfo.sampler_id', read_only=True)
    clinical_id = serializers.CharField(source='clinicalinfo.clinical_id', read_only=True)

    class Meta:
        model = FollowupInfo
        fields = ('clinical_id', 'sampler_id', 'survival_status', 'death_date', 'death_bool', 'recur_bool',
                  'recur_date', 'recur_status', 'followup_date', 'followup_status', 'memo', 'id', 'last_modify_time',
                  'create_time', 'sampleinventoryinfo', 'clinicalinfo')


class LiverPathologicalInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    sampler_id = serializers.CharField(source='sampleinventoryinfo.sampler_id', read_only=True)
    clinical_id = serializers.CharField(source='clinicalinfo.clinical_id', read_only=True)

    class Meta:
        model = LiverPathologicalInfo
        fields = ('pathological_id', 'clinical_id', 'sampler_id', 'check_date', 'check_stage', 'category', 'stage',
                  'tumor_count', 'tumor1_diam', 'tumor2_diam', 'tumor3_diam', 'capsule', 'lmr', 'lmr_category',
                  'vi_bool', 'bv_bool', 'mvi_category', 'section', 'G_score', 'S_score', 'memo', 'id',
                  'last_modify_time', 'create_time', 'sampleinventoryinfo', 'clinicalinfo')


class TMDInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    sampler_id = serializers.CharField(source='sampleinventoryinfo.sampler_id', read_only=True)
    clinical_id = serializers.CharField(source='clinicalinfo.clinical_id', read_only=True)

    class Meta:
        model = TMDInfo
        fields = ('clinical_id', 'sampler_id', 'check_date', 'check_stage', 'check_item1', 'check_item2',
                  'check_item3', 'check_item4', 'check_item5', 'check_item6', 'check_item7', 'check_item8',
                  'check_item9', 'check_item10', 'check_item11', 'check_item12', 'memo', 'id', 'last_modify_time',
                  'create_time', 'sampleinventoryinfo', 'clinicalinfo')


class BiochemInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    sampler_id = serializers.CharField(source='sampleinventoryinfo.sampler_id', read_only=True)
    clinical_id = serializers.CharField(source='clinicalinfo.clinical_id', read_only=True)

    class Meta:
        model = BiochemInfo
        fields = ('clinical_id', 'sampler_id', 'check_date', 'check_stage', 'check_item1', 'check_item2', 'check_item3',
                  'check_item4', 'check_item5', 'check_item6', 'check_item7', 'check_item8', 'check_item9',
                  'check_item10', 'check_item11', 'check_item12', 'memo', 'id', 'last_modify_time', 'create_time',
                  'sampleinventoryinfo', 'clinicalinfo')

