from django.db import models


# Create your models here.
class ClinicalInfo(models.Model):
    clinical_id = models.CharField(
        db_column='病历编号', unique=True, max_length=80, blank=True, null=True)
    sampleinventoryinfo = models.ForeignKey(
        "BIS.SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='ClinicalInfo_BIS2SampleInventoryInfo',
        db_column='样本库存信息',
        blank=True,
        null=True)
    patientId = models.CharField(
        db_column='住院号', max_length=35)
    hospital = models.CharField(
        db_column='医院编号', max_length=50)
    department = models.CharField(
        db_column='科室', max_length=50, blank=True, null=True)
    name = models.CharField(
        db_column='姓名', max_length=35, blank=True, null=True)
    gender = models.CharField(
        db_column='性别', max_length=2, blank=True, null=True, default='男')
    age = models.IntegerField(db_column='年龄', blank=True, null=True)
    record_date = models.DateField(
        db_column='记录日期', blank=True, null=True)
    category = models.CharField(db_column='癌种', max_length=50, blank=True, null=True)
    stage = models.CharField(db_column='分化程度', max_length=15, blank=True, null=True)
    tumor1_diam = models.FloatField(db_column='肿瘤最大径', blank=True, null=True)
    TNM = models.CharField(db_column='TNM分期', max_length=15, blank=True, null=True)
    AJCC = models.CharField(db_column='AJCC分期', max_length=15, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return self.clinical_id

    class Meta:
        db_table = '基本临床信息表'
        verbose_name = '基本临床信息表'
        ordering = ['-id']
        permissions = [
            ("bulk_delete_ClinicalInfo", "Can bulk delete 基本临床信息表"),
            ("bulk_update_ClinicalInfo", "Can bulk update 基本临床信息表"),
        ]


class FollowupInfo(models.Model):
    clinicalinfo = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='FollowupInfo_ClinicalInfo',
        db_column='基本临床信息',
        blank=True,
        null=True)
    sampleinventoryinfo = models.ForeignKey(
        "BIS.SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='FollowupInfo_BIS2SampleInventoryInfo',
        db_column='样本库存信息',
        blank=True,
        null=True)
    survival_status = models.CharField(
        db_column='生存状态', max_length=10, blank=True, null=True, default="存活")
    death_date = models.DateField(
        db_column='死亡日期', blank=True, null=True)
    death_bool = models.CharField(
        db_column='死因是否与肿瘤相关', max_length=10, blank=True, null=True, default="否")
    death_reason = models.CharField(
        db_column='死亡原因', max_length=255, blank=True, null=True)
    recur_bool = models.CharField(
        db_column='是否复发', max_length=10, blank=True, null=True, default="否")
    recur_date = models.DateField(
        db_column='复发日期', blank=True, null=True)
    recur_position = models.CharField(
        db_column='复发转移部位', max_length=255, blank=True, null=True)
    recur_status = models.CharField(
        db_column='复发状态', max_length=255, blank=True, null=True)
    followup_date = models.DateField(
        db_column='随访日期', blank=True, null=True)
    followup_status = models.CharField(
        db_column='随访情况', max_length=255, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return "{}_{}".format(self.clinicalinfo.clinical_id, self.followup_date)

    class Meta:
        db_table = '随访信息表'
        verbose_name = '随访信息表'
        ordering = ['-id']
        permissions = [
            ("bulk_delete_FollowupInfo", "Can bulk delete 随访信息表"),
            ("bulk_update_FollowupInfo", "Can bulk update 随访信息表"),
        ]


class LiverPathologicalInfo(models.Model):
    pathological_id = models.CharField(
        db_column='病理报告编号', unique=True, max_length=35, blank=True, null=True)
    clinicalinfo = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='LiverPathologicalInfo_ClinicalInfo',
        db_column='基本临床信息',
        blank=True,
        null=True)
    sampleinventoryinfo = models.ForeignKey(
        "BIS.SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='LiverPathologicalInfo_BIS2SampleInventoryInfo',
        db_column='样本库存信息',
        blank=True,
        null=True)
    raw_id = models.CharField(db_column='病理编号', max_length=50, blank=True, null=True)
    check_date = models.DateField(
        db_column='检查日期', blank=True, null=True)
    check_stage = models.CharField(
        db_column='检查阶段', max_length=255, blank=True, null=True)
    category = models.CharField(db_column='病理类型', max_length=50, blank=True, null=True)
    stage = models.CharField(db_column='分化程度', max_length=15, blank=True, null=True)
    tumor_count = models.PositiveIntegerField(db_column='肿瘤数目', default=0)
    tumor1_diam = models.FloatField(db_column='肿瘤最大径', blank=True, null=True)
    tumor2_diam = models.FloatField(db_column='肿瘤2直径', blank=True, null=True)
    tumor3_diam = models.FloatField(db_column='肿瘤3直径', blank=True, null=True)
    capsule = models.CharField(db_column='肝包膜侵犯(肝被膜)', max_length=15, blank=True, null=True)
    lmr = models.CharField(db_column='淋巴结转移', max_length=255, blank=True, null=True)
    lmr_category = models.CharField(db_column='淋巴结转移类型', max_length=15, blank=True, null=True)
    vi_bool = models.CharField(
        db_column='肉眼癌栓(脉管侵犯)', max_length=1, blank=True, null=True, default="否")
    bv_bool = models.CharField(
        db_column='微血管浸润', max_length=1, blank=True, null=True, default="否")
    mvi_category = models.CharField(db_column='MVI风险等级', max_length=255, blank=True, null=True)
    section = models.CharField(db_column='切面距癌距离(切除面)', max_length=255, blank=True, null=True)
    G_score = models.CharField(db_column='G评分', max_length=15, blank=True, null=True)
    S_score = models.CharField(db_column='S评分', max_length=15, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return self.pathological_id

    class Meta:
        db_table = '肝癌病理报告信息表'
        verbose_name = '肝癌病理报告信息表'
        ordering = ['-id']
        permissions = [
            ("bulk_delete_LiverPathologicalInfo", "Can bulk delete 肝癌病理报告信息表"),
            ("bulk_update_LiverPathologicalInfo", "Can bulk update 肝癌病理报告信息表"),
        ]


class TMDInfo(models.Model):
    clinicalinfo = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='TMDInfo_ClinicalInfo',
        db_column='基本临床信息',
        blank=True,
        null=True)
    sampleinventoryinfo = models.ForeignKey(
        "BIS.SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='TMDInfo_BIS2SampleInventoryInfo',
        db_column='样本库存信息',
        blank=True,
        null=True)
    check_date = models.DateField(
        db_column='检查日期')
    check_stage = models.CharField(
        db_column='检查阶段', max_length=255, blank=True, null=True)
    check_item1 = models.CharField(
        db_column='甲胎蛋白', max_length=255, blank=True, null=True)
    check_item2 = models.CharField(
        db_column='甲胎蛋白异质体', max_length=255, blank=True, null=True)
    check_item3 = models.CharField(
        db_column='癌胚抗原', max_length=255, blank=True, null=True)
    check_item4 = models.CharField(
        db_column='糖类抗原19-9', max_length=255, blank=True, null=True)
    check_item5 = models.CharField(
        db_column='黑素瘤抑制蛋白', max_length=255, blank=True, null=True)
    check_item6 = models.CharField(
        db_column='细胞角蛋白19片段', max_length=255, blank=True, null=True)
    check_item7 = models.CharField(
        db_column='糖类抗原125', max_length=255, blank=True, null=True)
    check_item8 = models.CharField(
        db_column='神经元特异性烯醇化酶', max_length=255, blank=True, null=True)
    check_item9 = models.CharField(
        db_column='鳞状细胞癌抗原', max_length=255, blank=True, null=True)
    check_item10 = models.CharField(
        db_column='胃泌素释放肽前体', max_length=255, blank=True, null=True)
    check_item11 = models.CharField(
        db_column='糖类抗原15-3', max_length=255, blank=True, null=True)
    check_item12 = models.CharField(
        db_column='前列腺特异性抗原', max_length=255, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return "{}_{}".format(self.clinicalinfo.clinical_id, self.check_date)

    class Meta:
        db_table = '肿瘤标志物检测结果信息表'
        verbose_name = '肿瘤标志物检测结果信息表'
        ordering = ['-id']
        permissions = [
            ("bulk_delete_TMDInfo", "Can bulk delete 肿瘤标志物检测结果信息表"),
            ("bulk_update_TMDInfo", "Can bulk update 肿瘤标志物检测结果信息表"),
        ]


class BiochemInfo(models.Model):
    clinicalinfo = models.ForeignKey(
        "ClinicalInfo",
        on_delete=models.CASCADE,
        related_name='BiochemInfo_ClinicalInfo',
        db_column='基本临床信息',
        blank=True,
        null=True)
    sampleinventoryinfo = models.ForeignKey(
        "BIS.SampleInventoryInfo",
        on_delete=models.CASCADE,
        related_name='BiochemInfo_BIS2SampleInventoryInfo',
        db_column='样本库存信息',
        blank=True,
        null=True)
    check_date = models.DateField(
        db_column='检查日期')
    check_stage = models.CharField(
        db_column='检查阶段', max_length=255, blank=True, null=True)
    check_item1 = models.CharField(
        db_column='总胆红素', max_length=255, blank=True, null=True)
    check_item2 = models.CharField(
        db_column='丙氨酸氨基转移酶', max_length=255, blank=True, null=True)
    check_item3 = models.CharField(
        db_column='γ-谷氨酰转移酶', max_length=255, blank=True, null=True)
    check_item4 = models.CharField(
        db_column='白蛋白', max_length=255, blank=True, null=True)
    check_item5 = models.CharField(
        db_column='α-L-岩藻糖苷酶', max_length=255, blank=True, null=True)
    check_item6 = models.CharField(
        db_column='直接胆红素', max_length=255, blank=True, null=True)
    check_item7 = models.CharField(
        db_column='谷丙转氨酶', max_length=255, blank=True, null=True)
    check_item8 = models.CharField(
        db_column='谷草转氨酶', max_length=255, blank=True, null=True)
    check_item9 = models.CharField(
        db_column='r-谷氨酰转肽酶', max_length=255, blank=True, null=True)
    check_item10 = models.CharField(
        db_column='碱性磷酸酶', max_length=255, blank=True, null=True)
    check_item11 = models.CharField(
        db_column='总胆汁酸', max_length=255, blank=True, null=True)
    check_item12 = models.CharField(
        db_column='前白蛋白', max_length=255, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return "{}_{}".format(self.clinicalinfo.clinical_id, self.check_date)

    class Meta:
        db_table = '肿瘤生化检测结果信息表'
        verbose_name = '生化检测结果信息表'
        ordering = ['-id']
        permissions = [
            ("bulk_delete_BiochemInfo", "Can bulk delete 生化检测结果信息表"),
            ("bulk_update_BiochemInfo", "Can bulk update 生化检测结果信息表"),
        ]
