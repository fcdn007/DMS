from django.db import models
from BIS.models import SampleInventoryInfo, SampleInfo, ExtractInfo
from LIMS.models import MethyLibraryInfo, MethyCaptureInfo, MethyPoolingInfo


# Create your models here.
class SequencingInfo(models.Model):
    sequencing_id = models.CharField(
        db_column='上机文库号', unique=True, max_length=35, blank=True, null=True)
    poolingLB_id = models.ManyToManyField(
        "LIMS.MethyCaptureInfo",
        related_name='SequencingInfo_LIMS2MethyCaptureInfo',
        db_column='捕获文库名',
        blank=True)
    send_date = models.DateField(db_column='送测日期', blank=True, null=True)
    start_time = models.DateField(db_column='上机时间', blank=True, null=True)
    end_time = models.DateField(db_column='下机时间', blank=True, null=True)
    machine_id = models.CharField(
        db_column='机器号', max_length=100, blank=True, null=True)
    chip_id = models.CharField(
        db_column='芯片号', max_length=100, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    index = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return self.sequencing_id

    class Meta:
        db_table = '测序登记表'
        verbose_name = '测序登记表'
        ordering = ['-index']
        permissions = [
            ("bulk_delete_SequencingInfo", "Can bulk delete 测序登记表"),
            ("bulk_update_SequencingInfo", "Can bulk update 测序登记表"),
        ]


# 表8 样本测序质控表
class MethyQCInfo(models.Model):
    QC_id = models.CharField(
        db_column='Sample', unique=True, max_length=35, blank=True, null=True)
    data_size_gb_field = models.FloatField(
        db_column='Data_Size-Gb', blank=True, null=True)
    clean_rate_field = models.FloatField(
        db_column='Clean_Rate', blank=True, null=True)
    r1_q20 = models.FloatField(db_column='R1_Q20', blank=True, null=True)
    r2_q20 = models.FloatField(db_column='R2_Q20', blank=True, null=True)
    r1_q30 = models.FloatField(db_column='R1_Q30', blank=True, null=True)
    r2_q30 = models.FloatField(db_column='R2_Q30', blank=True, null=True)
    gc_content = models.FloatField(
        db_column='GC_Content', blank=True, null=True)
    bs_conversion_rate_lambda_dna_field = models.FloatField(
        db_column='BS_conversion_rate-lambda_DNA', blank=True, null=True)
    bs_conversion_rate_chh_field = models.FloatField(
        db_column='BS_conversion_rate-CHH', blank=True, null=True)
    bs_conversion_rate_chg_field = models.FloatField(
        db_column='BS_conversion_rate-CHG', blank=True, null=True)
    uniquely_paired_mapping_rate = models.FloatField(
        db_column='Uniquely_Paired_Mapping_Rate', blank=True, null=True)
    mismatch_and_indel_rate = models.FloatField(
        db_column='Mismatch_and_InDel_Rate', blank=True, null=True)
    mode_fragment_length_bp_field = models.FloatField(
        db_column='Mode_Fragment_Length-bp', blank=True, null=True)
    genome_duplication_rate = models.FloatField(
        db_column='Genome_Duplication_Rate', blank=True, null=True)
    genome_depth_x_field = models.FloatField(
        db_column='Genome_Depth', blank=True, null=True)
    genome_dedupped_depth_x_field = models.FloatField(
        db_column='Genome_Dedupped_Depth', blank=True, null=True)
    genome_coverage = models.FloatField(
        db_column='Genome_Coverage', blank=True, null=True)
    genome_4x_cpg_depth_x_field = models.FloatField(
        db_column='Genome_4X_CpG_Depth', blank=True, null=True)
    genome_4x_cpg_coverage = models.FloatField(
        db_column='Genome_4X_CpG_Coverage', blank=True, null=True)
    genome_4x_cpg_methylation_level = models.FloatField(
        db_column='Genome_4X_CpG_methylation_level', blank=True, null=True)
    panel_4x_cpg_depth_x_field = models.FloatField(
        db_column='Panel_4X_CpG_Depth', blank=True, null=True)
    panel_4x_cpg_coverage = models.FloatField(
        db_column='Panel_4X_CpG_Coverage', blank=True, null=True)
    panel_4x_cpg_methylation_level = models.FloatField(
        db_column='Panel_4X_CpG_methylation_level', blank=True, null=True)
    panel_ontarget_rate_region_field = models.FloatField(
        db_column='Panel_Ontarget_Rate-region', blank=True, null=True)
    panel_duplication_rate_region_field = models.FloatField(
        db_column='Panel_Duplication_Rate-region', blank=True, null=True)
    panel_depth_site_x_field = models.FloatField(
        db_column='Panel_Depth-site_X', blank=True, null=True)
    panel_dedupped_depth_site_x_field = models.FloatField(
        db_column='Panel_Dedupped_Depth-site_X', blank=True, null=True)
    panel_coverage_site_1x_field = models.FloatField(
        db_column='Panel_Coverage-site_1X', blank=True, null=True)
    panel_coverage_site_10x_field = models.FloatField(
        db_column='Panel_Coverage-site_10X', blank=True, null=True)
    panel_coverage_site_20x_field = models.FloatField(
        db_column='Panel_Coverage-site_20X', blank=True, null=True)
    panel_coverage_site_50x_field = models.FloatField(
        db_column='Panel_Coverage-site_50X', blank=True, null=True)
    panel_coverage_site_100x_field = models.FloatField(
        db_column='Panel_Coverage-site_100X', blank=True, null=True)
    panel_uniformity_site_20_mean_field = models.FloatField(
        db_column='Panel_Uniformity-site_gt0.2mean', blank=True, null=True)
    strand_balance_f_field = models.FloatField(
        db_column='Strand_balance-F', blank=True, null=True)
    strand_balance_r_field = models.FloatField(
        db_column='Strand_balance-R', blank=True, null=True)
    gc_bin_depth_ratio = models.FloatField(
        db_column='GC_bin_depth_ratio', blank=True, null=True)
    sampler_id = models.ForeignKey(
        "BIS.SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='MethyQCInfo_BIS2SampleInventoryInfo',
        to_field="sampler_id",
        db_column='患者编号',
        blank=True,
        null=True)
    sample_id = models.ForeignKey(
        "BIS.SampleInfo",
        on_delete=models.CASCADE,
        related_name='MethyQCInfo_BIS2SampleInfo',
        to_field="sample_id",
        db_column='样本编号',
        blank=True,
        null=True)
    dna_id = models.ForeignKey(
        "BIS.ExtractInfo",
        on_delete=models.CASCADE,
        related_name='MethyQCInfo_BIS2ExtractInfo',
        to_field="dna_id",
        db_column='核酸提取编号',
        blank=True,
        null=True)
    singleLB_id = models.ForeignKey(
        "LIMS.MethyLibraryInfo",
        on_delete=models.CASCADE,
        related_name='MethyQCInfo_LIMS2MethyLibraryInfo',
        to_field="singleLB_id",
        db_column='建库编号',
        blank=True,
        null=True)
    poolingLB_id = models.ForeignKey(
        "LIMS.MethyCaptureInfo",
        on_delete=models.CASCADE,
        related_name='MethyQCInfo_LIMS2MethyCaptureInfo',
        to_field="poolingLB_id",
        db_column='捕获文库名',
        blank=True,
        null=True)
    singleLB_Pooling_id = models.ForeignKey(
        "LIMS.MethyPoolingInfo",
        on_delete=models.CASCADE,
        related_name='MethyQCInfo_LIMS2MethyPoolingInfo',
        to_field="singleLB_Pooling_id",
        db_column='测序文库名',
        blank=True,
        null=True)
    sequencing_id = models.ForeignKey(
        "SequencingInfo",
        on_delete=models.CASCADE,
        related_name='MethyQCInfo_SequencingInfo',
        to_field="sequencing_id",
        db_column='上机文库号',
        blank=True,
        null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    index = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return self.QC_id

    class Meta:
        db_table = '样本甲基化检测测序质控表'
        verbose_name = '样本甲基化检测测序质控表'
        ordering = ['-index']
        permissions = [
            ("bulk_delete_SequencingInfo", "Can bulk delete 样本甲基化检测测序质控表"),
            ("bulk_update_SequencingInfo", "Can bulk update 样本甲基化检测测序质控表"),
        ]
