# Generated by Django 2.1.7 on 2020-06-30 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BIS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MethyCaptureInfo',
            fields=[
                ('poolingLB_id', models.CharField(blank=True, db_column='捕获文库名', max_length=35, null=True, unique=True)),
                ('hybrid_date', models.DateField(blank=True, db_column='杂交日期', null=True)),
                ('probes', models.CharField(blank=True, db_column='杂交探针', max_length=50, null=True)),
                ('hybrid_min', models.FloatField(blank=True, db_column='杂交时间', null=True)),
                ('postpcr_cycles', models.IntegerField(blank=True, db_column='PostPCR循环数', null=True)),
                ('postpcr_con', models.FloatField(blank=True, db_column='PostPCR浓度', null=True)),
                ('elution_vol', models.FloatField(blank=True, db_column='洗脱体积', null=True)),
                ('operator', models.CharField(blank=True, db_column='操作人', max_length=35, null=True)),
                ('memo', models.TextField(blank=True, db_column='备注', null=True)),
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_column='创建时间')),
                ('last_modify_time', models.DateTimeField(auto_now=True, db_column='最近修改时间')),
            ],
            options={
                'verbose_name': '甲基化捕获文库信息表',
                'db_table': '甲基化捕获文库信息表',
                'ordering': ['-index'],
            },
        ),
        migrations.CreateModel(
            name='MethyLibraryInfo',
            fields=[
                ('singleLB_id', models.CharField(blank=True, db_column='建库编号', max_length=35, null=True, unique=True)),
                ('tube_id', models.CharField(blank=True, db_column='管上编号', max_length=35, null=True)),
                ('clinical_boolen', models.CharField(blank=True, db_column='是否临床', default=1, max_length=25, null=True)),
                ('label', models.CharField(blank=True, db_column='样本标签', max_length=25, null=True)),
                ('singleLB_name', models.CharField(blank=True, db_column='文库名', max_length=35, null=True)),
                ('barcodes', models.CharField(blank=True, db_column='index列表', max_length=25, null=True)),
                ('LB_date', models.DateField(blank=True, db_column='建库日期', null=True)),
                ('LB_method', models.CharField(blank=True, db_column='建库方法', max_length=50, null=True)),
                ('kit_batch', models.CharField(blank=True, db_column='试剂批次', max_length=50, null=True)),
                ('mass', models.FloatField(blank=True, db_column='起始量', null=True)),
                ('pcr_cycles', models.IntegerField(blank=True, db_column='PCR循环数', null=True)),
                ('LB_con', models.FloatField(blank=True, db_column='文库浓度', null=True)),
                ('LB_vol', models.FloatField(blank=True, db_column='文库体积', null=True)),
                ('operator', models.CharField(blank=True, db_column='操作人', max_length=35, null=True)),
                ('memo', models.TextField(blank=True, db_column='备注', null=True)),
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_column='创建时间')),
                ('last_modify_time', models.DateTimeField(auto_now=True, db_column='最近修改时间')),
                ('dna_id', models.ForeignKey(blank=True, db_column='核酸提取编号', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyLibraryInfo_BIS2ExtractInfo', to='BIS.ExtractInfo', to_field='dna_id')),
                ('sample_id', models.ForeignKey(blank=True, db_column='样本编号', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyLibraryInfo_BIS2SampleInfo', to='BIS.SampleInfo', to_field='sample_id')),
                ('sampler_id', models.ForeignKey(blank=True, db_column='患者编号', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyLibraryInfo_BIS2SampleInventoryInfo', to='BIS.SampleInventoryInfo', to_field='sampler_id')),
            ],
            options={
                'verbose_name': '甲基化建库表',
                'db_table': '甲基化建库表',
                'ordering': ['-index'],
            },
        ),
        migrations.CreateModel(
            name='MethyPoolingInfo',
            fields=[
                ('singleLB_Pooling_id', models.CharField(blank=True, db_column='测序文库编号', max_length=35, null=True, unique=True)),
                ('pooling_ratio', models.FloatField(blank=True, db_column='pooling比例', null=True)),
                ('mass', models.FloatField(blank=True, db_column='取样', null=True)),
                ('volume', models.FloatField(blank=True, db_column='体积', null=True)),
                ('memo', models.TextField(blank=True, db_column='备注', null=True)),
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_column='创建时间')),
                ('last_modify_time', models.DateTimeField(auto_now=True, db_column='最近修改时间')),
                ('dna_id', models.ForeignKey(blank=True, db_column='核酸提取编号', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyPoolingInfo_BIS2ExtractInfo', to='BIS.ExtractInfo', to_field='dna_id')),
                ('poolingLB_id', models.ForeignKey(blank=True, db_column='捕获文库名', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyPoolingInfo_MethyCaptureInfo', to='LIMS.MethyCaptureInfo', to_field='poolingLB_id')),
                ('sample_id', models.ForeignKey(blank=True, db_column='样本编号', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyPoolingInfo_BIS2SampleInfo', to='BIS.SampleInfo', to_field='sample_id')),
                ('sampler_id', models.ForeignKey(blank=True, db_column='患者编号', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyPoolingInfo_BIS2SampleInventoryInfo', to='BIS.SampleInventoryInfo', to_field='sampler_id')),
                ('singleLB_id', models.ForeignKey(blank=True, db_column='建库编号', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MethyPoolingInfo_MethyLibraryInfo', to='LIMS.MethyLibraryInfo', to_field='singleLB_id')),
            ],
            options={
                'verbose_name': '甲基化pooling表',
                'db_table': '甲基化pooling表',
                'ordering': ['-index'],
            },
        ),
    ]
