from django.conf import settings
from rest_framework import serializers

from .models import ClinicalInfo, FollowupInfo, LiverPathologicalInfo, LiverTMDInfo, LiverBiochemInfo
from util.serializers import DynamicFieldsModelSerializer


class ClinicalInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = ClinicalInfo
        fields = ('clinical_id', 'sampler_id', 'patientId', 'hospital', 'department', 'name', 'gender', 'age',
                  'record_date', 'category', 'stage', 'tumor1_diam', 'memo', 'index', 'last_modify_time', 'create_time')


class FollowupInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = FollowupInfo
        fields = ('followup_id', 'clinical_id', 'sampler_id', 'survival_status', 'death_date', 'death_bool',
                  'recur_bool', 'recur_date', 'recur_status', 'followup_date', 'followup_status', 'memo', 'index',
                  'last_modify_time', 'create_time')


class LiverPathologicalInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = LiverPathologicalInfo
        fields = ('pathological_id', 'clinical_id', 'sampler_id', 'check_date', 'check_stage', 'category', 'stage',
                  'tumor_count', 'tumor1_diam', 'tumor2_diam', 'tumor3_diam', 'capsule', 'lmr', 'lmr_category',
                  'vi_bool', 'bv_bool', 'mvi_category', 'section', 'G_score', 'S_score', 'memo', 'index',
                  'last_modify_time', 'create_time')


class LiverTMDInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = LiverTMDInfo
        fields = ('check_id', 'clinical_id', 'sampler_id', 'check_date', 'check_stage', 'check_item1', 'check_item2',
                  'check_item3', 'check_item4', 'check_item5', 'check_item6', 'check_item7', 'check_item8',
                  'check_item9', 'check_item10', 'check_item11', 'check_item12', 'memo', 'index', 'last_modify_time',
                  'create_time')


class LiverBiochemInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = LiverBiochemInfo
        fields = ('check_id', 'clinical_id', 'sampler_id', 'check_date', 'check_stage', 'check_item1', 'check_item2',
                  'check_item3', 'check_item4', 'check_item5', 'check_item6', 'check_item7', 'check_item8',
                  'check_item9', 'check_item10', 'check_item11', 'check_item12', 'memo', 'index', 'last_modify_time',
                  'create_time')

