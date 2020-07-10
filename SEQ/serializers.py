from django.conf import settings
from rest_framework import serializers

from util.serializers import DynamicFieldsModelSerializer
from .models import SequencingInfo, MethyQCInfo


class SequencingInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    poolingLB_id = serializers.SerializerMethodField()

    def get_poolingLB_id(self, obj):
        names = []
        for q_ in obj.methycaptureinfo.all():
            names.append(q_.poolingLB_id)
        return ", ".join(names)

    class Meta:
        model = SequencingInfo
        fields = ('sequencing_id', 'poolingLB_id', 'send_date', 'start_time', 'end_time', 'machine_id', 'chip_id',
                  'memo', 'id', 'last_modify_time', 'create_time', 'methycaptureinfo')


class MethyQCInfoSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    sampler_id = serializers.CharField(source='sampleinventoryinfo.sampler_id', read_only=True)
    singleLB_Pooling_id = serializers.CharField(source='methypoolinginfo.singleLB_Pooling_id', read_only=True)
    sequencing_id = serializers.CharField(source='sequencinginfo.sequencing_id', read_only=True)

    class Meta:
        model = MethyQCInfo
        fields = ('QC_id', 'data_size_gb_field', 'clean_rate_field', 'r1_q20', 'r2_q20', 'r1_q30', 'r2_q30',
                  'gc_content', 'bs_conversion_rate_lambda_dna_field', 'bs_conversion_rate_chh_field',
                  'bs_conversion_rate_chg_field', 'uniquely_paired_mapping_rate', 'mismatch_and_indel_rate',
                  'mode_fragment_length_bp_field', 'genome_duplication_rate', 'genome_depth_x_field',
                  'genome_dedupped_depth_x_field', 'genome_coverage', 'genome_4x_cpg_depth_x_field',
                  'genome_4x_cpg_coverage', 'genome_4x_cpg_methylation_level', 'panel_4x_cpg_depth_x_field',
                  'panel_4x_cpg_coverage', 'panel_4x_cpg_methylation_level', 'panel_ontarget_rate_region_field',
                  'panel_duplication_rate_region_field', 'panel_depth_site_x_field',
                  'panel_dedupped_depth_site_x_field', 'panel_coverage_site_1x_field', 'panel_coverage_site_10x_field',
                  'panel_coverage_site_20x_field', 'panel_coverage_site_50x_field', 'panel_coverage_site_100x_field',
                  'panel_uniformity_site_20_mean_field', 'strand_balance_f_field', 'strand_balance_r_field',
                  'gc_bin_depth_ratio', 'sampler_id', 'singleLB_Pooling_id', 'sequencing_id', 'memo', 'id',
                  'last_modify_time', 'create_time', 'sampleinventoryinfo', 'methypoolinginfo', 'sequencing_id')
