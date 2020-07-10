# Generated by Django 3.0.7 on 2020-07-07 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('LIMS', '0001_initial'),
        ('BIS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SequencingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequencing_id', models.CharField(blank=True, db_column='上机文库号', max_length=35, null=True, unique=True)),
                ('send_date', models.DateField(blank=True, db_column='送测日期', null=True)),
                ('start_time', models.DateField(blank=True, db_column='上机时间', null=True)),
                ('end_time', models.DateField(blank=True, db_column='下机时间', null=True)),
                ('machine_id', models.CharField(blank=True, db_column='机器号', max_length=100, null=True)),
                ('chip_id', models.CharField(blank=True, db_column='芯片号', max_length=100, null=True)),
                ('memo', models.TextField(blank=True, db_column='备注', null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_column='创建时间')),
                ('last_modify_time', models.DateTimeField(auto_now=True, db_column='最近修改时间')),
                ('methycaptureinfo', models.ManyToManyField(blank=True, db_column='甲基化捕获文库信息', related_name='SequencingInfo_LIMS2MethyCaptureInfo', to='LIMS.MethyCaptureInfo')),
            ],
            options={
                'verbose_name': '测序登记信息表',
                'db_table': '测序登记信息表',
                'ordering': ['-id'],
                'permissions': [('bulk_delete_SequencingInfo', 'Can bulk delete 测序登记信息表'), ('bulk_update_SequencingInfo', 'Can bulk update 测序登记信息表')],
            },
        ),
        migrations.CreateModel(
            name='MethyQCInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QC_id', models.CharField(blank=True, db_column='Sample', max_length=35, null=True, unique=True)),
                ('data_size_gb_field', models.FloatField(blank=True, db_column='Data_Size-Gb', null=True)),
                ('clean_rate_field', models.FloatField(blank=True, db_column='Clean_Rate', null=True)),
                ('r1_q20', models.FloatField(blank=True, db_column='R1_Q20', null=True)),
                ('r2_q20', models.FloatField(blank=True, db_column='R2_Q20', null=True)),
                ('r1_q30', models.FloatField(blank=True, db_column='R1_Q30', null=True)),
                ('r2_q30', models.FloatField(blank=True, db_column='R2_Q30', null=True)),
                ('gc_content', models.FloatField(blank=True, db_column='GC_Content', null=True)),
                ('bs_conversion_rate_lambda_dna_field', models.FloatField(blank=True, db_column='BS_conversion_rate-lambda_DNA', null=True)),
                ('bs_conversion_rate_chh_field', models.FloatField(blank=True, db_column='BS_conversion_rate-CHH', null=True)),
                ('bs_conversion_rate_chg_field', models.FloatField(blank=True, db_column='BS_conversion_rate-CHG', null=True)),
                ('uniquely_paired_mapping_rate', models.FloatField(blank=True, db_column='Uniquely_Paired_Mapping_Rate', null=True)),
                ('mismatch_and_indel_rate', models.FloatField(blank=True, db_column='Mismatch_and_InDel_Rate', null=True)),
                ('mode_fragment_length_bp_field', models.FloatField(blank=True, db_column='Mode_Fragment_Length-bp', null=True)),
                ('genome_duplication_rate', models.FloatField(blank=True, db_column='Genome_Duplication_Rate', null=True)),
                ('genome_depth_x_field', models.FloatField(blank=True, db_column='Genome_Depth', null=True)),
                ('genome_dedupped_depth_x_field', models.FloatField(blank=True, db_column='Genome_Dedupped_Depth', null=True)),
                ('genome_coverage', models.FloatField(blank=True, db_column='Genome_Coverage', null=True)),
                ('genome_4x_cpg_depth_x_field', models.FloatField(blank=True, db_column='Genome_4X_CpG_Depth', null=True)),
                ('genome_4x_cpg_coverage', models.FloatField(blank=True, db_column='Genome_4X_CpG_Coverage', null=True)),
                ('genome_4x_cpg_methylation_level', models.FloatField(blank=True, db_column='Genome_4X_CpG_methylation_level', null=True)),
                ('panel_4x_cpg_depth_x_field', models.FloatField(blank=True, db_column='Panel_4X_CpG_Depth', null=True)),
                ('panel_4x_cpg_coverage', models.FloatField(blank=True, db_column='Panel_4X_CpG_Coverage', null=True)),
                ('panel_4x_cpg_methylation_level', models.FloatField(blank=True, db_column='Panel_4X_CpG_methylation_level', null=True)),
                ('panel_ontarget_rate_region_field', models.FloatField(blank=True, db_column='Panel_Ontarget_Rate-region', null=True)),
                ('panel_duplication_rate_region_field', models.FloatField(blank=True, db_column='Panel_Duplication_Rate-region', null=True)),
                ('panel_depth_site_x_field', models.FloatField(blank=True, db_column='Panel_Depth-site_X', null=True)),
                ('panel_dedupped_depth_site_x_field', models.FloatField(blank=True, db_column='Panel_Dedupped_Depth-site_X', null=True)),
                ('panel_coverage_site_1x_field', models.FloatField(blank=True, db_column='Panel_Coverage-site_1X', null=True)),
                ('panel_coverage_site_10x_field', models.FloatField(blank=True, db_column='Panel_Coverage-site_10X', null=True)),
                ('panel_coverage_site_20x_field', models.FloatField(blank=True, db_column='Panel_Coverage-site_20X', null=True)),
                ('panel_coverage_site_50x_field', models.FloatField(blank=True, db_column='Panel_Coverage-site_50X', null=True)),
                ('panel_coverage_site_100x_field', models.FloatField(blank=True, db_column='Panel_Coverage-site_100X', null=True)),
                ('panel_uniformity_site_20_mean_field', models.FloatField(blank=True, db_column='Panel_Uniformity-site_gt0.2mean', null=True)),
                ('strand_balance_f_field', models.FloatField(blank=True, db_column='Strand_balance-F', null=True)),
                ('strand_balance_r_field', models.FloatField(blank=True, db_column='Strand_balance-R', null=True)),
                ('gc_bin_depth_ratio', models.FloatField(blank=True, db_column='GC_bin_depth_ratio', null=True)),
                ('memo', models.TextField(blank=True, db_column='备注', null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_column='创建时间')),
                ('last_modify_time', models.DateTimeField(auto_now=True, db_column='最近修改时间')),
                ('methypoolinginfo', models.ForeignKey(blank=True, db_column='甲基化pooling信息', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyQCInfo_LIMS2MethyPoolingInfo', to='LIMS.MethyPoolingInfo')),
                ('sampleinventoryinfo', models.ForeignKey(blank=True, db_column='样本库存信息', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyQCInfo_BIS2SampleInventoryInfo', to='BIS.SampleInventoryInfo')),
                ('sequencinginfo', models.ForeignKey(blank=True, db_column='测序登记信息', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyQCInfo_SequencingInfo', to='SEQ.SequencingInfo')),
            ],
            options={
                'verbose_name': '甲基化检测测序质控信息表',
                'db_table': '甲基化检测测序质控信息表',
                'ordering': ['-id'],
                'permissions': [('bulk_delete_MethyQCInfo', 'Can bulk delete 甲基化检测测序质控信息表'), ('bulk_update_MethyQCInfo', 'Can bulk update 甲基化检测测序质控信息表')],
            },
        ),
    ]
