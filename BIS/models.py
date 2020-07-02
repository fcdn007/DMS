from django.db import models


# Create your models here.
# 表1 样本库存信息表
class SampleInventoryInfo(models.Model):
    sampler_id = models.CharField(
        db_column='患者编号', unique=True, max_length=35, blank=True, null=True)
    plasma_num = models.PositiveIntegerField(db_column='血浆管数', default=0)
    adjacent_mucosa_num = models.PositiveIntegerField(
        db_column='癌旁组织', default=0)
    cancer_tissue_num = models.PositiveIntegerField(db_column='癌组织', default=0)
    WBC_num = models.PositiveIntegerField(db_column='白细胞', default=0)
    stool_num = models.PositiveIntegerField(db_column='粪便', default=0)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    index = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return self.sampler_id

    class Meta:
        db_table = '样本库存信息表'
        verbose_name = '样本库存信息表'
        ordering = ['-index']
        permissions = [
            ("bulk_delete_SampleInventoryInfo", "Can bulk delete 样本库存信息表"),
            ("bulk_update_SampleInventoryInfo", "Can bulk update 样本库存信息表"),
        ]


# 表2 样本信息表
class SampleInfo(models.Model):
    sample_id = models.CharField(
        db_column='样本编号', unique=True, max_length=35, blank=True, null=True)
    sampler_id = models.ForeignKey(
        "SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='SampleInfo_SampleInventoryInfo',
        to_field="sampler_id",
        db_column='患者编号',
        blank=True,
        null=True)
    raw_id = models.CharField(
        db_column='原始样本编号', max_length=50, blank=True, null=True)
    fridge = models.CharField(db_column='冰箱位置', max_length=50)
    plate = models.CharField(db_column='孔板号', max_length=50)
    well = models.CharField(db_column='孔位', max_length=50)
    sample_type = models.CharField(db_column='样本类型', max_length=50)
    sample_date = models.DateField(db_column='采样日期', blank=True, null=True)
    send_date = models.DateField(db_column='寄送日期', blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    index = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True, db_column='创建时间')
    last_modify_time = models.DateTimeField(auto_now=True, db_column='最近修改时间')

    def __str__(self):
        return self.sample_id

    class Meta:
        db_table = '样本信息表'
        verbose_name = '样本信息表'
        ordering = ['-index']
        permissions = [
            ("bulk_delete_SampleInfo", "Can bulk delete 样本信息表"),
            ("bulk_update_SampleInfo", "Can bulk update 样本信息表"),
        ]


# 表3 样本提取表
class ExtractInfo(models.Model):
    dna_id = models.CharField(db_column='核酸提取编号', unique=True, max_length=35)
    sampler_id = models.ForeignKey(
        "SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='ExtractInfo_SampleInventoryInfo',
        to_field="sampler_id",
        db_column='患者编号',
        blank=True,
        null=True)
    sample_id = models.ForeignKey(
        "SampleInfo",
        on_delete=models.CASCADE,
        related_name='ExtractInfo_SampleInfo',
        to_field="sample_id",
        db_column='样本编号',
        blank=True,
        null=True)
    extract_date = models.DateField(db_column='提取日期', blank=True, null=True)
    sample_type = models.CharField(db_column='样本类型', max_length=50)
    nucleic_type = models.CharField(db_column='核酸类型', max_length=50)
    sample_volume = models.FloatField(db_column='样本体积', blank=True, null=True)
    extract_method = models.CharField(
        db_column='提取方法', max_length=50, blank=True, null=True)
    dna_con = models.FloatField(db_column='浓度', blank=True, null=True)
    dna_vol = models.FloatField(db_column='体积', blank=True, null=True)
    fridge = models.CharField(db_column='冰箱位置', max_length=50)
    plate = models.CharField(db_column='孔板号', max_length=50)
    well = models.CharField(db_column='孔位', max_length=50)
    successM = models.FloatField(db_column='成功建库使用量', blank=True, null=True)
    failM = models.FloatField(db_column='失败建库使用量', blank=True, null=True)
    researchM = models.FloatField(db_column='科研项目使用量', blank=True, null=True)
    othersM = models.FloatField(db_column='其他使用量', blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    index = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return self.dna_id

    class Meta:
        db_table = '样本提取表'
        verbose_name = '样本提取表'
        ordering = ['-index']
        permissions = [
            ("bulk_delete_ExtractInfo", "Can bulk delete 样本提取表"),
            ("bulk_update_ExtractInfo", "Can bulk update 样本提取表"),
        ]


# 表4 样本核酸使用记录表
class DNAUsageRecordInfo(models.Model):
    dna_id = models.ForeignKey(
        "ExtractInfo",
        on_delete=models.CASCADE,
        related_name='DNAUsageRecordInfo_ExtractInfo',
        to_field="dna_id",
        db_column='核酸提取编号',
        blank=True,
        null=True)
    sampler_id = models.ForeignKey(
        "SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='DNAUsageRecordInfo_SampleInventoryInfo',
        to_field="sampler_id",
        db_column='患者编号',
        blank=True,
        null=True)
    sample_id = models.ForeignKey(
        "SampleInfo",
        on_delete=models.CASCADE,
        related_name='DNAUsageRecordInfo_SampleInfo',
        to_field="sample_id",
        db_column='样本编号',
        blank=True,
        null=True)
    usage_date = models.DateField(db_column='使用日期', blank=True, null=True)
    mass = models.FloatField(db_column='使用量', blank=True, null=True)
    usage = models.CharField(db_column='用途', max_length=25)
    singleLB_id = models.CharField(
        db_column='建库编号', max_length=35, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    index = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return ":".join([str(self.dna_id), str(self.index)])

    class Meta:
        db_table = '样本核酸使用记录表'
        verbose_name = '样本核酸使用记录表'
        ordering = ['-index']
        permissions = [
            ("bulk_delete_DNAUsageRecordInfo", "Can bulk delete 样本核酸使用记录表"),
            ("bulk_update_DNAUsageRecordInfo", "Can bulk update 样本核酸使用记录表"),
        ]
