from django.db import models


# Create your models here.
class MethyLibraryInfo(models.Model):
    singleLB_id = models.CharField(
        db_column='建库编号', unique=True, max_length=35, blank=True, null=True)
    sampleinventoryinfo = models.ForeignKey(
        "BIS.SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='MethyLibraryInfo_BIS2SampleInventoryInfo',
        db_column='样本库存信息',
        blank=True,
        null=True)
    extractinfo = models.ForeignKey(
        "BIS.ExtractInfo",
        on_delete=models.CASCADE,
        related_name='MethyLibraryInfo_BIS2ExtractInfo',
        db_column='核酸提取编号',
        blank=True,
        null=True)
    tube_id = models.CharField(
        db_column='管上编号', max_length=35, blank=True, null=True)
    clinical_boolen = models.CharField(
        db_column='是否临床', max_length=25, blank=True, null=True, default=1)
    label = models.CharField(
        db_column='样本标签', max_length=25, blank=True, null=True)
    singleLB_name = models.CharField(
        db_column='文库名', max_length=35, blank=True, null=True)
    barcodes = models.CharField(
        db_column='index列表', max_length=25, blank=True, null=True)
    LB_date = models.DateField(db_column='建库日期', blank=True, null=True)
    LB_method = models.CharField(
        db_column='建库方法', max_length=50, blank=True, null=True)
    kit_batch = models.CharField(
        db_column='试剂批次', max_length=50, blank=True, null=True)
    mass = models.FloatField(db_column='起始量(ng)', blank=True, null=True)
    pcr_cycles = models.IntegerField(db_column='PCR循环数', blank=True, null=True)
    LB_con = models.FloatField(db_column='文库浓度(ng/ul)', blank=True, null=True)
    LB_vol = models.FloatField(db_column='文库体积(ul)', blank=True, null=True)
    operator = models.CharField(
        db_column='操作人', max_length=35, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return self.singleLB_id

    class Meta:
        db_table = '甲基化建库信息表'
        verbose_name = '甲基化建库信息表'
        ordering = ['-id']
        permissions = [
            ("bulk_delete_MethyLibraryInfo", "Can bulk delete 甲基化建库信息表"),
            ("bulk_update_MethyLibraryInfo", "Can bulk update 甲基化建库信息表"),
        ]


# 表5 甲基化捕获文库信息表
class MethyCaptureInfo(models.Model):
    poolingLB_id = models.CharField(
        db_column='捕获文库名',
        unique=True,
        max_length=35,
        blank=True,
        null=True)
    hybrid_date = models.DateField(db_column='杂交日期', blank=True, null=True)
    probes = models.CharField(
        db_column='杂交探针', max_length=50, blank=True, null=True)
    hybrid_min = models.FloatField(db_column='杂交时间(min)', blank=True, null=True)
    postpcr_cycles = models.IntegerField(
        db_column='PostPCR循环数', blank=True, null=True)
    postpcr_con = models.FloatField(
        db_column='PostPCR浓度(ng/ul)', blank=True, null=True)
    elution_vol = models.FloatField(db_column='洗脱体积(ul)', blank=True, null=True)
    operator = models.CharField(
        db_column='操作人', max_length=35, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return self.poolingLB_id

    class Meta:
        db_table = '甲基化捕获文库信息表'
        verbose_name = '甲基化捕获文库信息表'
        ordering = ['-id']
        permissions = [
            ("bulk_delete_MethyCaptureInfo", "Can bulk delete 甲基化捕获文库信息表"),
            ("bulk_update_MethyCaptureInfo", "Can bulk update 甲基化捕获文库信息表"),
        ]


# 表6 pooling表
class MethyPoolingInfo(models.Model):
    methylibraryinfo = models.ForeignKey(
        "MethyLibraryInfo",
        on_delete=models.CASCADE,
        related_name='MethyPoolingInfo_MethyLibraryInfo',
        db_column='甲基化建库信息',
        blank=True,
        null=True)
    methycaptureinfo = models.ForeignKey(
        "MethyCaptureInfo",
        on_delete=models.CASCADE,
        related_name='MethyPoolingInfo_MethyCaptureInfo',
        db_column='甲基化捕获文库信息',
        blank=True,
        null=True)
    singleLB_Pooling_id = models.CharField(
        db_column='测序文库编号', unique=True, max_length=80, blank=True, null=True)
    sampleinventoryinfo = models.ForeignKey(
        "BIS.SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='SampleInfo_BIS2SampleInventoryInfo',
        db_column='样本库存信息',
        blank=True,
        null=True)
    pooling_ratio = models.FloatField(db_column='pooling比例', blank=True, null=True)
    mass = models.FloatField(db_column='取样(ng)', blank=True, null=True)
    volume = models.FloatField(db_column='体积(ul)', blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return self.singleLB_Pooling_id

    class Meta:
        db_table = '甲基化pooling信息表'
        verbose_name = '甲基化pooling信息表'
        ordering = ['-id']
        permissions = [
            ("bulk_delete_MethyPoolingInfo", "Can bulk delete 甲基化pooling信息表"),
            ("bulk_update_MethyPoolingInfo", "Can bulk update 甲基化pooling信息表"),
        ]
