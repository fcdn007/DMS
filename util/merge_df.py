import os
import re
import subprocess
import time
from collections import defaultdict

import numpy as np
import pandas as pd
from django.forms.models import model_to_dict

from BIS.models import *
from EMR.models import *
from LIMS.models import *
from SEQ.models import *
from databaseDemo.settings import MEDIA_ROOT

models_set = [SampleInventoryInfo, SampleInfo, ExtractInfo, DNAUsageRecordInfo, MethyLibraryInfo, MethyCaptureInfo,
              MethyPoolingInfo, SequencingInfo, MethyQCInfo, ClinicalInfo, FollowupInfo, LiverPathologicalInfo,
              TMDInfo, BiochemInfo]

apps_models_index = [[0, 1, 2, 3], [4, 6, 5], [7, 8], [9, 10, 11, 12, 13]]

apps = ["BIS", "LIMS", "SEQ", "EMR"]

models_update_index = {
    "SampleInventoryInfo": ["sampler_id"], "SampleInfo": ["sample_id"], "ExtractInfo": ["dna_id"],
    "DNAUsageRecordInfo": ["extractinfo", "usage", "usage_date"], "MethyLibraryInfo": ["singleLB_id"],
    "MethyCaptureInfo": ["poolingLB_id"], "MethyPoolingInfo": ["singleLB_Pooling_id"],
    "SequencingInfo": ["sequencing_id"], "MethyQCInfo": ["QC_id"], "ClinicalInfo": ["clinical_id"],
    "FollowupInfo": ["clinicalinfo", "followup_date"], "LiverPathologicalInfo": ["pathological_id"],
    "TMDInfo": ["clinicalinfo", "check_date"], "BiochemInfo": ["clinicalinfo", "check_date"]
}

models_set2 = []

FILECOLUMN_TO_FIELD = {
    'normal': {},
    'foreign': {
        'SampleInfo': {
            '华大编号': 'sampler_id'
        },
        'ExtractInfo': {
            '生物样本编号': 'sample_id'
        },
        'DNAUsageRecordInfo': {
            '核酸提取编号': 'dna_id'
        },
        'MethyLibraryInfo': {
            '核酸提取编号': 'dna_id',
        },
        'MethyPoolingInfo': {
            '建库编号': 'singleLB_id',
            '捕获文库名': 'poolingLB_id'
        },
        'SequencingInfo': {
            '捕获文库名': 'poolingLB_id'
        },
        'MethyQCInfo': {
            '上机文库号': 'sequencing_id',
            '测序文库名': 'singleLB_Pooling_id'
        },
        'ClinicalInfo': {
            '华大编号': 'sampler_id'
        },
        'FollowupInfo': {
            '病历编号': 'clinical_id'
        },
        'LiverPathologicalInfo': {
            '病历编号': 'clinical_id'
        },
        'TMDInfo': {
            '病历编号': 'clinical_id'
        },
        'BiochemInfo': {
            '病历编号': 'clinical_id'
        }
    },
    'foreignAdd': {
        'ExtractInfo': {
            '华大编号': [SampleInfo, 'sample_id', '生物样本编号', 'sampleinventoryinfo', 'sampler_id']
        },
        'DNAUsageRecordInfo': {
            '华大编号': [ExtractInfo, 'dna_id', '核酸提取编号', 'sampleinventoryinfo', 'sampler_id'],
        },
        'MethyLibraryInfo': {
            '华大编号': [ExtractInfo, 'dna_id', '核酸提取编号', 'sampleinventoryinfo', 'sampler_id'],
        },
        'MethyPoolingInfo': {
            '华大编号': [MethyLibraryInfo, 'singleLB_id', '建库编号', 'sampleinventoryinfo', 'sampler_id'],
        },
        'MethyQCInfo': {
            '华大编号': [MethyPoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'sampleinventoryinfo', 'sampler_id'],
        },
        'FollowupInfo': {
            '华大编号': [ClinicalInfo, 'clinical_id', '病历编号', 'sampleinventoryinfo', 'sampler_id']
        },
        'LiverPathologicalInfo': {
            '华大编号': [ClinicalInfo, 'clinical_id', '病历编号', 'sampleinventoryinfo', 'sampler_id']
        },
        'TMDInfo': {
            '华大编号': [ClinicalInfo, 'clinical_id', '病历编号', 'sampleinventoryinfo', 'sampler_id']
        },
        'BiochemInfo': {
            '华大编号': [ClinicalInfo, 'clinical_id', '病历编号', 'sampleinventoryinfo', 'sampler_id']
        }
    },
    'normalAdd': {}
}

FILECOLUMN_FOREIGNKEY_TO_MODEL = {
    'sampler_id': SampleInventoryInfo,
    'sample_id': SampleInfo,
    'dna_id': ExtractInfo,
    'singleLB_id': MethyLibraryInfo,
    'poolingLB_id': MethyCaptureInfo,
    'singleLB_Pooling_id': MethyPoolingInfo,
    'sequencing_id': SequencingInfo,
    'clinical_id': ClinicalInfo
}

FOREIGNKEY_CONVERSION = {
    'sampler_id': "sampleinventoryinfo",
    'sample_id': "sampleinfo",
    'dna_id': "extractinfo",
    'singleLB_id': "methylibraryinfo",
    'poolingLB_id': "methycaptureinfo",
    'singleLB_Pooling_id': "methypoolinginfo",
    'sequencing_id': "sequencinginfo",
    'clinical_id': "clinicalinfo",
    "sampleinventoryinfo": ['sampler_id', '华大编号'],
    "sampleinfo": ['sample_id', '生物样本编号'],
    "extractinfo": ['dna_id', '核酸提取编号'],
    "methylibraryinfo": ['singleLB_id', '建库编号'],
    "methycaptureinfo": ['poolingLB_id', '捕获文库名'],
    "methypoolinginfo": ['singleLB_Pooling_id', '测序文库名'],
    "sequencinginfo": ['sequencing_id', '上机文库号'],
    "clinicalinfo": ['clinical_id', '病历编号']
}

KEY1_TO_MODEL = {}

FIELD_CLASS = {}

for model_ in models_set:
    # 字符串化model名称作为字典的键
    k = str(model_).split(" ")[1].split(".")[2].split("'")[0]
    # 获得list：字符串化model名称
    models_set2.append(k)
    # 字符串化model名称 -> model
    KEY1_TO_MODEL[k] = model_
    FIELD_CLASS[k] = {
        "emptyDrop_list": [], "repeatDrop_list": [], "str_list": [], "num_list": [], "date_list": []
    }
    FILECOLUMN_TO_FIELD["normal"][k] = {}
    if k == 'ExtractInfo':
        FILECOLUMN_TO_FIELD["normalAdd"][k] = {}
    for field in model_._meta.fields:
        if field.name in ["id", "create_time", "last_modify_time"]:
            continue
        elif type(field).__name__ == "ForeignKey":
            db_name = FOREIGNKEY_CONVERSION[field.name][1]
            if db_name in FILECOLUMN_TO_FIELD['foreign'][k]:
                FIELD_CLASS[k]["emptyDrop_list"].append(db_name)
            continue
        elif k == 'ExtractInfo' and field.name in ["successM", "failM", "researchM", "othersM"]:
            FILECOLUMN_TO_FIELD["normalAdd"][k][field.db_column] = [field.name, "num"]
            continue
        elif field.name in FILECOLUMN_FOREIGNKEY_TO_MODEL and \
                str(FILECOLUMN_FOREIGNKEY_TO_MODEL[field.name]).split(" ")[1].split(".")[2].split("'")[0] == k:
            FIELD_CLASS[k]["repeatDrop_list"].append(field.db_column)
            FIELD_CLASS[k]["emptyDrop_list"].append(field.db_column)
            FILECOLUMN_TO_FIELD["normal"][k][field.db_column] = field.name
            continue

        FILECOLUMN_TO_FIELD["normal"][k][field.db_column] = field.name
        if type(field).__name__ == "TextField" or type(field).__name__ == "CharField":
            FIELD_CLASS[k]["str_list"].append(field.db_column)
        elif type(field).__name__ == "FloatField" or type(field).__name__ == "PositiveIntegerField":
            FIELD_CLASS[k]["num_list"].append(field.db_column)
        elif type(field).__name__ == "DateField":
            FIELD_CLASS[k]["date_list"].append(field.db_column)

FIELD_CLASS["DNAUsageRecordInfo"]["emptyDrop_list"] = FIELD_CLASS["DNAUsageRecordInfo"]["emptyDrop_list"] + \
                                                       ['用途', '使用日期']
FIELD_CLASS["DNAUsageRecordInfo"]["repeatDrop_list"] = ['核酸提取编号', '用途', '使用日期']
FIELD_CLASS["SequencingInfo"]["emptyDrop_list"].append('捕获文库名')
FIELD_CLASS["ClinicalInfo"]["emptyDrop_list"] = FIELD_CLASS["ClinicalInfo"]["emptyDrop_list"] + \
                                                       ['住院号', '医院编号']
FIELD_CLASS["ClinicalInfo"]["repeatDrop_list"] = FIELD_CLASS["ClinicalInfo"]["repeatDrop_list"] + \
                                                       ['住院号', '医院编号']
FIELD_CLASS["FollowupInfo"]["repeatDrop_list"] = ["病历编号", "随访日期"]
FIELD_CLASS["LiverPathologicalInfo"]["emptyDrop_list"].append("病理报告编号")
FIELD_CLASS["LiverPathologicalInfo"]["repeatDrop_list"] = ["病理报告编号", "病历编号"]
FIELD_CLASS["TMDInfo"]["repeatDrop_list"] = ["病历编号", "检查日期"]
FIELD_CLASS["BiochemInfo"]["repeatDrop_list"] = ["病历编号", "检查日期"]


def clean_data(data_, warning_msg_dict, error_msg_dict, skip_list, params):
    emptyDrop_list = params["emptyDrop_list"]
    repeatDrop_list = params["repeatDrop_list"]
    str_list = params["str_list"]
    num_list = params["num_list"]
    date_list = params["date_list"]
    data = data_.copy(deep=True)
    repeatKey_dict = defaultdict(list)
    # deal with error_msg_dict['emptyKey']
    for row in range(data.shape[0]):
        emptyDrop_list_exists = 0
        for col in emptyDrop_list:
            if col not in data:
                skip_list[row] = 1
                if col in error_msg_dict['emptyKey']:
                    error_msg_dict['emptyKey'][col].append(u'第{}行'.format(row + 2))
                else:
                    error_msg_dict['emptyKey'][col] = [u'第{}行'.format(row + 2)]
                continue

            emptyDrop_list_exists += 1
            try:
                if pd.isnull(data[col][row]):
                    skip_list[row] = 1
                    if col in error_msg_dict['emptyKey']:
                        error_msg_dict['emptyKey'][col].append(u'第{}行'.format(row + 2))
                    else:
                        error_msg_dict['emptyKey'][col] = [u'第{}行'.format(row + 2)]
            except ValueError:
                if isinstance(data[col][row], list) and len(data[col][row]) == 0:
                    skip_list[row] = 1
                    if col in error_msg_dict['emptyKey']:
                        error_msg_dict['emptyKey'][col].append(u'第{}行'.format(row + 2))
                    else:
                        error_msg_dict['emptyKey'][col] = [u'第{}行'.format(row + 2)]
        # deal with error_msg_dict['repeatKey']
        if emptyDrop_list_exists == len(emptyDrop_list):
            if len(repeatDrop_list) > 0:
                key = '/ '.join([str(data[col][row]) for col in repeatDrop_list])
                if key in repeatKey_dict:
                    repeatKey_dict[key].append(row)
                else:
                    repeatKey_dict[key] = [row]

    for key in repeatKey_dict:
        if len(repeatKey_dict[key]) > 1:
            row_list = []
            for row in repeatKey_dict[key]:
                skip_list[row] = 1
                row_list.append(u'第{}行'.format(row + 2))
            error_msg_dict['repeatKey']['/ '.join(repeatDrop_list)].append('({})'.format(', '.join(row_list)))

    # deal with warning_msg_dict['empty'] and warning_msg_dict['invalid']
    for id1 in str_list:
        if id1 not in data:
            data[id1] = ['无' for x in range(data.shape[0])]
            continue

        col_data = []
        for id2 in range(len(data[id1])):
            if pd.isnull(data[id1][id2]):
                col_data.append('无')
            else:
                col_data.append(str(data[id1][id2]).strip())
        data[id1] = col_data

    for id1 in num_list:
        if id1 not in data:
            data[id1] = [9999 for x in range(data.shape[0])]
            continue

        col_data = []
        for id2 in range(len(data[id1])):
            m1 = re.match(r'^(\d+)[^0-9]+$', str(data[id1][id2]).strip())
            m2 = re.match(r'^(\d+\.\d+)[^0-9]+$', str(data[id1][id2]).strip())
            # 判断数值为空
            if pd.isnull(data[id1][id2]) or str(data[id1][id2]).strip() == '-' or str(data[id1][id2]).strip() == '-%' \
                    or re.match(r'^-bp$', str(data[id1][id2]).strip(), flags=re.IGNORECASE):
                col_data.append(9999)
            elif pd.api.types.is_number(data[id1][id2]):
                col_data.append(data[id1][id2])
            elif re.match(r'^\d+$', str(data[id1][id2])) or re.match(r'^\d+\.0+$', str(data[id1][id2])):
                col_data.append(int(data[id1][id2]))
            elif re.match(r'^\d+\.\d+$', str(data[id1][id2])) or re.match(r'^-?\d[eE][+-]\d+$', str(data[id1][id2])):
                col_data.append(float(data[id1][id2]))
            elif m1:
                col_data.append(int(m1.group(1)))
            elif m2:
                col_data.append(float(m2.group(1)))
            else:
                col_data.append(9999)
                warning_msg_dict['invalid'].append(u'第{}行"{}"列'.format(id2 + 2, id1))
        data[id1] = col_data

    # data[id] = [0 if pd.isnull(x) else x for x in data[id]]
    for id1 in date_list:
        if id1 not in data:
            data[id1] = ['2000-01-01' for x in range(data.shape[0])]
            continue

        col_data = []
        for id2 in range(len(data[id1])):
            try:
                col_data.append(pd.to_datetime(data[id1][id2]).strftime("%Y-%m-%d"))
            except ValueError:
                m1 = re.match(r'^(\d{4})(\d{2})(\d{2})', str(data[id1][id2]))
                m2 = re.match(r'^(\d{4}).(\d{2}).(\d{2})', str(data[id1][id2]))
                m3 = re.match(r'^(\d{4})-(\d{2})-(\d{2})', str(data[id1][id2]))
                if pd.isnull(data[id1][id2]):
                    col_data.append('2000-01-01')
                elif m1:
                    col_data.append("%s-%s-%s" % (m1.group(1), m1.group(2), m1.group(3)))
                elif m2:
                    col_data.append("%s-%s-%s" % (m2.group(1), m2.group(2), m2.group(3)))
                elif m3:
                    col_data.append("%s-%s-%s" % (m3.group(1), m3.group(2), m3.group(3)))
                else:
                    col_data.append('2000-01-01')
                    warning_msg_dict['invalid'].append(u'第{}行"{}"列'.format(id2 + 2, id1))
        data[id1] = col_data
    return data


def read_file(url, inf, warning_msg_dict, error_msg_dict):
    # 读取文件，按文件类型调用不同函数打开
    df = []
    ext = inf.split('.')[-1].lower()
    if ext == "txt":
        df = pd.read_table(inf, sep="\t", header=0, encoding='utf-8')
    elif ext == "csv":
        df = pd.read_csv(inf, header=0, encoding='utf-8')
    elif ext == "xlsx":
        df = pd.read_excel(inf, header=0, encoding='utf-8')
    # 根据url，进行数据清洗
    data = []
    skip_list = [0 for x in range(df.shape[0])]
    fatal_error = ""
    if url in models_set2:
        cols = list(FILECOLUMN_TO_FIELD['normal'][url].keys())
        if url in FILECOLUMN_TO_FIELD['foreign']:
            cols = cols + list(FILECOLUMN_TO_FIELD['foreign'][url].keys())
        try:
            data = df.loc[:, cols].copy(deep=True)
            if len(FIELD_CLASS[url]['repeatDrop_list']) > 0:
                error_msg_dict['repeatKey']['/ '.join(FIELD_CLASS[url]['repeatDrop_list'])] = []
            if url == "SequencingInfo":
                data.loc[:, '捕获文库名'] = [[y.strip() for y in x.split(',')] for x in data.loc[:, '捕获文库名']]
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list, FIELD_CLASS[url])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'MethyCaptureInfoPlus':
        cols = list(set(list(FILECOLUMN_TO_FIELD['normal']['MethyCaptureInfo'].keys()) +
                        list(FILECOLUMN_TO_FIELD['normal']['MethyPoolingInfo'].keys()) +
                        list(FILECOLUMN_TO_FIELD['foreign']['MethyPoolingInfo'].keys())))
        try:
            data = df.loc[:, cols].copy(deep=True)
            params = {
                "emptyDrop_list": FIELD_CLASS["MethyPoolingInfo"]['emptyDrop_list'],
                "repeatDrop_list": FIELD_CLASS["MethyPoolingInfo"]['repeatDrop_list'],
                "str_list": FIELD_CLASS["MethyCaptureInfo"]['str_list'] + FIELD_CLASS["MethyPoolingInfo"]['str_list'],
                "num_list": FIELD_CLASS["MethyCaptureInfo"]['num_list'] + FIELD_CLASS["MethyPoolingInfo"]['num_list'],
                "date_list": FIELD_CLASS["MethyCaptureInfo"]['date_list'] + FIELD_CLASS["MethyPoolingInfo"]['date_list']
            }
            error_msg_dict['repeatKey']['/ '.join(params['repeatDrop_list'])] = []
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list, params)
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    return data, skip_list, fatal_error


def save_records(upload_file):
    warning_msg = ""
    warning_msg_dict = defaultdict(list)
    error_msg = ""
    error_msg_dict = defaultdict(dict)
    # 读取文件，进行数据清洗
    records, skip_list, fatal_error = read_file(
        upload_file.uploadUrl, upload_file.uploadFile.path, warning_msg_dict, error_msg_dict)

    if fatal_error:
        return 'NA', 'NA', 'NA', '', '', fatal_error

    add_list = []
    context_pre = {}
    for row in range(records.shape[0]):
        if skip_list[row]:
            continue

        context = {}
        many2many_list = []
        created = False
        next_bool = False
        if upload_file.uploadUrl in FILECOLUMN_TO_FIELD['normal']:
            # 数据预处理
            if upload_file.uploadUrl in FILECOLUMN_TO_FIELD['foreign']:
                for db_column in FILECOLUMN_TO_FIELD['foreign'][upload_file.uploadUrl]:
                    model_key = FILECOLUMN_TO_FIELD['foreign'][upload_file.uploadUrl][db_column]
                    # 获取foreignKey对应的object
                    # print('upload_file.uploadUrl: %s; model_key: %s' % (upload_file.uploadUrl, model_key))
                    if not (upload_file.uploadUrl == 'SequencingInfo' and model_key == 'poolingLB_id'):
                        # print('model: {}; key: {}; value: {}'.format(FOREIGNKEY_TO_MODEL[model_key], model_key,
                        # records[col][row]))
                        try:
                            obj_ = FILECOLUMN_FOREIGNKEY_TO_MODEL[model_key].objects.get(
                                **{model_key: records[db_column][row]})
                            # print(obj_)
                            context[FOREIGNKEY_CONVERSION[model_key]] = obj_
                        except FILECOLUMN_FOREIGNKEY_TO_MODEL[model_key].DoesNotExist:
                            if db_column in error_msg_dict:
                                error_msg_dict['noForeignKey'][db_column].append(u'第{}行'.format(row + 2))
                            else:
                                error_msg_dict['noForeignKey'][db_column] = [u'第{}行'.format(row + 2)]
                            # print("change skip_list[{}] to 1".format(row))
                            skip_list[row] = 1
                            next_bool = True
                            break
                    else:
                        for c in records['捕获文库名'][row]:
                            try:
                                many2many_list.append(
                                    MethyCaptureInfo.objects.get(poolingLB_id=c))
                            except MethyCaptureInfo.DoesNotExist:
                                warning_msg_dict['empty'].append(
                                    u'第{}行"{}"列的"{}"'.format(row + 2, u'捕获文库名', c))

            if next_bool:
                # print("skip row {} from next_bool".format(row))
                # print(skip_list)
                continue

            for db_column in FILECOLUMN_TO_FIELD['normal'][upload_file.uploadUrl]:
                context[FILECOLUMN_TO_FIELD['normal'][upload_file.uploadUrl][db_column]] = records[db_column][row]

            if upload_file.uploadUrl in FILECOLUMN_TO_FIELD['foreignAdd']:
                # 对于输入文件中缺少的外键k1，
                # 先找到输入文件中存在的外键k2，
                # 再通过k2对应的model2找到k1对应的值value1
                # 再通过k1对应的model1找到相应对象
                for db_column in FILECOLUMN_TO_FIELD['foreignAdd'][upload_file.uploadUrl]:
                    list_ = FILECOLUMN_TO_FIELD['foreignAdd'][upload_file.uploadUrl][db_column]
                    value = model_to_dict(list_[0].objects.get(**{list_[1]: records[list_[2]][row]}))[list_[3]]
                    obj_ = FILECOLUMN_FOREIGNKEY_TO_MODEL[list_[4]].objects.get(id=value)
                    context[list_[3]] = obj_

            # 模型增/改
            if upload_file.uploadUrl in ["SampleInventoryInfo", "SampleInfo", "ExtractInfo", "MethyCaptureInfo",
                                         "MethyPoolingInfo", "MethyQCInfo", "ClinicalInfo", "FollowupInfo",
                                         "LiverPathologicalInfo", "TMDInfo", "BiochemInfo"]:
                # 添加/更新
                obj_dict = {}
                for field_ in models_update_index[upload_file.uploadUrl]:
                    obj_dict[field_] = context[field_]

                _, created = KEY1_TO_MODEL[upload_file.uploadUrl].objects.update_or_create(
                    **obj_dict, defaults={**context})
            elif upload_file.uploadUrl == 'DNAUsageRecordInfo':
                # 修改提取表
                extractinfo = ExtractInfo.objects.get(dna_id=context['dna_id'])
                try:  # PUT，改
                    usageRecord = DNAUsageRecordInfo.objects.get(
                        extractinfo=extractinfo,
                        usage=context['usage'],
                        usage_date=context['usage_date']
                    )
                    mass_ = float(context['mass']) - usageRecord.mass
                except DNAUsageRecordInfo.DoesNotExist:  # POST，增
                    mass_ = float(context['mass'])
                if context['usage'] == '建库失败':
                    extractinfo.failM = extractinfo.failM + mass_
                elif context['usage'] == '科研项目':
                    extractinfo.researchM = extractinfo.researchM + mass_
                elif context['usage'] == '其他':
                    extractinfo.othersM = extractinfo.othersM + mass_
                extractinfo.save()
                # 添加/修改使用记录表
                obj_dict = {}
                for field_ in models_update_index[upload_file.uploadUrl]:
                    obj_dict[field_] = context[field_]

                _, created = KEY1_TO_MODEL[upload_file.uploadUrl].objects.update_or_create(
                    **obj_dict, defaults={**context})

            elif upload_file.uploadUrl == 'MethyLibraryInfo':
                # 添加/修改甲基化建库表
                obj_dict = {}
                for field_ in models_update_index[upload_file.uploadUrl]:
                    obj_dict[field_] = context[field_]

                _, created = KEY1_TO_MODEL[upload_file.uploadUrl].objects.update_or_create(
                    **obj_dict, defaults={**context})

                # 修改使用记录表
                try:  # PUT，改
                    usageRecord = DNAUsageRecordInfo.objects.get(
                        singleLB_id=context['singleLB_id']
                    )
                    sub_ = float(context["mass"]) - usageRecord.mass
                    usageRecord.mass = usageRecord.mass + sub_
                    if usageRecord.usage_date != context["usage_date"]:
                        usageRecord.usage_date = context["usage_date"]
                    usageRecord.save()
                    mass_inventory = sub_
                except DNAUsageRecordInfo.DoesNotExist:  # POST，增
                    context2 = {
                        'sampleinventoryinfo': context['sampleinventoryinfo'], 'extractinfo': context['extractinfo'],
                        'usage_date': context["LB_date"], 'mass': context["mass"],
                        'usage': '建库成功', 'singleLB_id': context["singleLB_id"],
                        'memo': context["memo"]
                    }
                    usageRecord = DNAUsageRecordInfo(**context2)
                    usageRecord.save()
                    mass_inventory = float(context["mass"])
                # 修改库存表
                extractinfo = context['extractinfo']
                extractinfo.successM = extractinfo.successM + mass_inventory
                extractinfo.save()
            elif upload_file.uploadUrl == 'SequencingInfo':
                # 添加/修改测序上机信息表
                obj_dict = {}
                for field_ in models_update_index[upload_file.uploadUrl]:
                    obj_dict[field_] = context[field_]

                sequencing, created = KEY1_TO_MODEL[upload_file.uploadUrl].objects.update_or_create(
                    **obj_dict, defaults={**context})
                sequencing.methycaptureinfo.add(*many2many_list)

            if created:
                add_list.append(row)
        else:
            if upload_file.uploadUrl == 'MethyCaptureInfoPlus':
                for model_ in ['MethyCaptureInfo', 'MethyPoolingInfo']:
                    # 数据预处理
                    context = {}
                    if model_ in FILECOLUMN_TO_FIELD['foreign']:
                        for db_column in FILECOLUMN_TO_FIELD['foreign'][model_]:
                            model_key = FILECOLUMN_TO_FIELD['foreign'][model_][db_column]
                            # 获取foreignKey对应的object
                            # print(">>>>>>>>>>>>>> notice >>>>>>>>>>>")
                            # pprint({model_key: records[db_column][row]})
                            try:
                                obj_ = FILECOLUMN_FOREIGNKEY_TO_MODEL[model_key].objects.get(
                                    **{model_key: records[db_column][row]})
                                context[model_key] = obj_
                            except FILECOLUMN_FOREIGNKEY_TO_MODEL[model_key].DoesNotExist:
                                if db_column in error_msg_dict:
                                    error_msg_dict['noForeignKey'][db_column].append(u'第{}行'.format(row + 2))
                                else:
                                    error_msg_dict['noForeignKey'][db_column] = [u'第{}行'.format(row + 2)]
                                skip_list[row] = 1
                                next_bool = True
                                break
                    if next_bool:
                        break

                    for db_column in FILECOLUMN_TO_FIELD['normal'][model_]:
                        context[FILECOLUMN_TO_FIELD['normal'][model_][db_column]] = records[db_column][row]

                    if model_ in FILECOLUMN_TO_FIELD['foreignAdd']:
                        for db_column in FILECOLUMN_TO_FIELD['foreignAdd'][model_]:
                            list_ = FILECOLUMN_TO_FIELD['foreignAdd'][model_][db_column]
                            value = model_to_dict(list_[0].objects.get(
                                **{list_[1]: records[list_[2]][row]}))[list_[3]]
                            obj_ = FILECOLUMN_FOREIGNKEY_TO_MODEL[list_[3]].objects.get(
                                **{list_[3]: value})
                            context[list_[3]] = obj_
                    # 模型增/改
                    if model_ == 'MethyCaptureInfo':
                        # 避免重复添加/更新捕获文库信息表
                        value_join = '; '.join([str(context[x]) for x in sorted(context.keys())])
                        if not (context['poolingLB_id'] in context_pre and context_pre[
                            context['poolingLB_id']] == value_join):
                            _, _ = MethyCaptureInfo.objects.update_or_create(
                                poolingLB_id=records[u'捕获文库名'][row], defaults={**context})
                            context_pre[context['poolingLB_id']] = value_join
                    else:
                        # print(">>>>>>>>>>>>> notice >>>>>>>>>>>", records[u'测序文库名'][row])
                        _, created = MethyPoolingInfo.objects.update_or_create(
                            singleLB_Pooling_id=records[u'测序文库名'][row], defaults={**context})

                if next_bool:
                    continue

                if created:
                    add_list.append(row)

    total = len(skip_list)
    valid = total - len([x for x in skip_list if x])
    # 输出 warning_msg, error_msg
    if len(warning_msg_dict['empty']) > 0:
        warning_msg += u'单元格为空或单元格值不存在：' + ', '.join(warning_msg_dict['empty'])
    if len(warning_msg_dict['invalid']) > 0:
        warning_msg += u'\n单元格值不符合格式：' + ', '.join(warning_msg_dict['invalid'])
    if len(error_msg_dict['repeatKey'].keys()) > 0 and \
            len(error_msg_dict['repeatKey'][list(error_msg_dict['repeatKey'].keys())[0]]) > 0:
        error_msg += u'存在重复关键字段的行：' + ', '.join(['{}({})'.format(key, ', '.join(
            error_msg_dict['repeatKey'][key])) for key in error_msg_dict['repeatKey']])
    if len(error_msg_dict['emptyKey'].keys()) > 0:
        error_msg += u'\n关键字段缺失或不正确：' + ', '.join(['{}({})'.format(key, ', '.join(
            error_msg_dict['emptyKey'][key])) for key in error_msg_dict['emptyKey']])
    if len(error_msg_dict['noForeignKey'].keys()) > 0:
        error_msg += u'\n关联对象不存在：' + ', '.join(['{}({})'.format(key, ', '.join(
            error_msg_dict['noForeignKey'][key])) for key in error_msg_dict['noForeignKey']])
    return total, valid, len(add_list), warning_msg, error_msg, fatal_error


def list2array(list_, names):
    array = []
    for i in list_:
        array.append(list(i))
    return pd.DataFrame(array, columns=names)


def check_new_merge_df_all():
    flag_update = []
    json_files = []
    time2 = []
    for idx in range(len(apps_models_index)):
        tmp = check_new_merge_df_partly(idx)
        flag_update.append(tmp[0])
        time2.append(tmp[1])
        json_files.append(tmp[2])
    return flag_update, time2, json_files


def check_new_merge_df_partly(idx):
    m_list = apps_models_index[idx]
    name = apps[idx]
    json_files = {}
    time2 = 0
    time2_len = {}
    for file in os.listdir(os.path.join(MEDIA_ROOT, "json")):
        if re.match(r'[0-9]+\.' + name + r'\.merge_df.json', file):
            time2_tmp = int(file.split('.')[0])
            json_files[time2_tmp] = os.path.join(MEDIA_ROOT, "json", file)
            if time2_tmp >= time2:
                time2 = time2_tmp
                time2_len = pd.read_json(os.path.join(MEDIA_ROOT, "json", re.sub(r'\.merge_df\.', '.model_len.', file))
                                         ).to_dict(orient='records')[0]

    lastTime_models = {}
    len_models = {}
    for m in m_list:
        len_models[models_set2[m]] = models_set[m].objects.count()
        if len_models[models_set2[m]] > 0:
            time_list = models_set[m].objects.values_list("last_modify_time").distinct().order_by("-last_modify_time")
            lastTime_models[models_set2[m]] = int(time_list[0][0].strftime("%Y%m%d%H%M%S%f"))
        else:
            lastTime_models[models_set2[m]] = 0

    flag_update = False
    for m in lastTime_models:
        if lastTime_models[m] > time2:
            if not flag_update:
                flag_update = True
            time2 = lastTime_models[m]
        if m not in time2_len or time2_len[m] != len_models[m]:
            if not flag_update:
                flag_update = True

    return [flag_update, time2, json_files]


def get_merge_df_cols(model_list):
    id_list = []
    name_list = []
    join_field_id_list = []
    join_field_name_list = []
    field_class_list = []
    plot_bool_list = []
    skip_plot_dict = {
        "SampleInfo": ["raw_id"],
        "MethyLibraryInfo": ["singleLB_name"],
        "ClinicalInfo": ["patientId", "name"],
        "LiverPathologicalInfo": ["pathological_id"]
    }
    for key_ in FOREIGNKEY_CONVERSION:
        if isinstance(FOREIGNKEY_CONVERSION[key_], list):
            join_field_id_list.append(FOREIGNKEY_CONVERSION[key_][0])
            join_field_name_list.append(FOREIGNKEY_CONVERSION[key_][1])
            field_class_list.append("str")
            plot_bool_list.append("false")
    for index_ in [y for x in apps_models_index for y in x]:
        model_str = models_set2[index_]
        normal_dict = FILECOLUMN_TO_FIELD["normal"][model_str]
        for db_name in normal_dict:
            if normal_dict[db_name] not in join_field_id_list:
                id_list.append("{}__{}".format(model_str, normal_dict[db_name]))
                name_list.append("{}-{}".format(models_set[index_]._meta.db_table, db_name))
                if db_name in FIELD_CLASS[model_str]["str_list"]:
                    field_class_list.append("str")
                elif db_name in FIELD_CLASS[model_str]["num_list"]:
                    field_class_list.append("num")
                elif db_name in FIELD_CLASS[model_str]["date_list"]:
                    field_class_list.append("date")
                else:
                    field_class_list.append("none")
                if (normal_dict[db_name] in ["memo", "create_time", "last_modify_time"]) or \
                        (model_str in skip_plot_dict and normal_dict[db_name] in skip_plot_dict[model_str]):
                    plot_bool_list.append("false")
                else:
                    plot_bool_list.append("true")

        if model_str in FILECOLUMN_TO_FIELD["normalAdd"]:
            id_list = id_list + ["{}__{}".format(model_str, x[0]) for x in
                FILECOLUMN_TO_FIELD["normalAdd"][model_str].values()]
            # ["ExtractInfo.successM", "ExtractInfo.failM", "ExtractInfo.researchM", "ExtractInfo.othersM"]
            name_list = name_list + ["{}-{}".format(models_set[index_]._meta.db_table, x) for x in
                FILECOLUMN_TO_FIELD["normalAdd"][model_str].keys()]
            field_class_list = field_class_list + [x[1] for x in FILECOLUMN_TO_FIELD["normalAdd"][model_str].values()]
            for id_ in [x[0] for x in FILECOLUMN_TO_FIELD["normalAdd"][model_str].values()]:
                if model_str in skip_plot_dict and id_ in skip_plot_dict[model_str]:
                    plot_bool_list.append("false")
                else:
                    plot_bool_list.append("true")
            # ["样本提取信息表-成功建库使用量(ng)", "样本提取信息表-失败建库使用量(ng)", "样本提取信息表-科研项目使用量(ng)",
            # "样本提取信息表-其他使用量(ng)"]
            # Todo: 增加key"fieldClass"，表示画图时字段对应的属性[str, num, date]
            # Todo: 增加key"plotBool"，表示是否允许用于画图
    id_merge_list = join_field_id_list+id_list
    name_merge_list = join_field_name_list+name_list
    keep_bool_list = [0 for x in range(len(id_merge_list))]
    for model_str in model_list:
        idx1 = models_set2.index(model_str)
        for field in models_set[idx1]._meta.fields:
            if field.name in ["id", "create_time", "last_modify_time"]:
                continue
            try:
                idx2 = id_merge_list.index(field.name)
            except ValueError:
                if field.name in FOREIGNKEY_CONVERSION and isinstance(FOREIGNKEY_CONVERSION[field.name], list):
                    idx2 = id_merge_list.index(FOREIGNKEY_CONVERSION[field.name][0])
                else:
                    idx2 = id_merge_list.index("{}__{}".format(model_str, field.name))
            if keep_bool_list[idx2] == 1:
                continue
            else:
                keep_bool_list[idx2] = 1
    keep_index_list = [x for x in range(len(keep_bool_list)) if keep_bool_list[x] == 1]
    return {
        "id": [id_merge_list[x] for x in keep_index_list],
        "name": [name_merge_list[x] for x in keep_index_list],
        "class": [field_class_list[x] for x in keep_index_list],
        "plot": [plot_bool_list[x] for x in keep_index_list]
    }


def make_new_merge_df_all(time2_list, json_files_list):
    # print("run make_new_merge_df_all in function")
    time_stamp = 0
    for t in range(4):
        if time2_list[t] > time_stamp:
            time_stamp = time2_list[t]
    running_file = os.path.join(MEDIA_ROOT, "json", '{}.ALL.merge_df.rebuild_running.status'.format(time_stamp))
    done_file = os.path.join(MEDIA_ROOT, "json", '{}.ALL.merge_df.rebuild_done.status'.format(time_stamp))
    if os.path.exists(running_file):
        while True:
            if os.path.exists(done_file):
                return True
            else:
                time.sleep(5)
    else:
        subprocess.run(["touch", running_file])
        subprocess.run("rm {}/*ALL*json".format(os.path.join(MEDIA_ROOT, "json")), shell=True)
    input_json_files = [json_files_list[0][time2_list[0]], json_files_list[1][time2_list[1]],
                        json_files_list[2][time2_list[2]], json_files_list[3][time2_list[3]]]
    df_list = []
    for i in range(4):
        df_list.append(pd.read_json(input_json_files[i]))
    join_cols = [["dna_id", "singleLB_id"], ["singleLB_Pooling_id", "poolingLB_id"], "sampler_id"]
    merge_df = df_list[0]
    for df_index in range(1, 4):
        if merge_df.shape[0] > 0 and df_list[df_index].shape[0] > 0:
            merge_df = pd.merge(merge_df, df_list[df_index], how='left', on=join_cols[df_index-1])
        else:
            for col_ in df_list[df_index].columns:
                if col_ not in merge_df.columns:
                    merge_df[col_] = [" " for row_ in range(merge_df.shape[0])]

    columns_raw = list(merge_df.columns)
    join_field_set = list(FILECOLUMN_FOREIGNKEY_TO_MODEL.keys())
    not_join_field_set = []
    for column in columns_raw:
        if column not in join_field_set:
            not_join_field_set.append(column)
    output_df = merge_df[join_field_set + not_join_field_set].fillna(" ")
    output_df.to_json(os.path.join(MEDIA_ROOT, "json", '{}.ALL.merge_df.json'.format(time_stamp)), date_format='iso')
    for input_json_file in input_json_files:
        input_json_file = re.sub(r'merge_df.json', "rebuild_done.status", input_json_file)
        if os.path.exists(input_json_file):
            subprocess.run(['rm', input_json_file])
    subprocess.run("rm {}/*.ALL.merge_df.rebuild_done.status".format(os.path.join(MEDIA_ROOT, "json")), shell=True)
    subprocess.run(["touch", done_file])
    subprocess.run(["rm", running_file])
    return True


def make_new_merge_df_partly(json_files_tmp, time2, index):
    running_file = os.path.join(MEDIA_ROOT, "json", '{}.{}.rebuild_running.status'.format(time2, apps[index]))
    done_file = os.path.join(MEDIA_ROOT, "json", '{}.{}.rebuild_done.status'.format(time2, apps[index]))
    if os.path.exists(running_file):
        while True:
            if os.path.exists(done_file):
                return True
            else:
                time.sleep(5)
    else:
        subprocess.run(["touch", running_file])
        subprocess.run("rm {}/*{}*json".format(os.path.join(MEDIA_ROOT, "json"), apps[index]), shell=True)
    merge_df_tmp = pd.DataFrame()
    len_models = {}
    models_set_index = apps_models_index[index]
    join_field_set = []
    for idx in models_set_index:
        model_str = models_set2[idx]
        fields = list(FILECOLUMN_TO_FIELD['normal'][model_str].values())
        # Todo: 提取表增加字段
        if model_str in FILECOLUMN_TO_FIELD["normalAdd"]:
            fields = fields[:-1] + [x[0] for x in FILECOLUMN_TO_FIELD["normalAdd"][model_str].values()] + [fields[-1]]
        join_field = ""
        last_idx = len(fields)
        if model_str in FILECOLUMN_TO_FIELD['foreign']:
            fields = fields + ["{}__{}".format(FOREIGNKEY_CONVERSION[x], x) for x in list(
                FILECOLUMN_TO_FIELD['foreign'][model_str].values())]
            if not join_field:
                join_field = fields[last_idx].split("__")[1]
        elif model_str == "MethyCaptureInfo":  # CaptureInfo需要特殊处理
            join_field = "poolingLB_id"
        res_raw = list(models_set[idx].objects.values_list(*fields))
        fields_rename = []
        for field_ in fields:
            if field_ in [FOREIGNKEY_CONVERSION[y] + "__" + y for y in FILECOLUMN_FOREIGNKEY_TO_MODEL]:
                fields_rename.append(field_.split("__")[1])
            elif field_ in FOREIGNKEY_CONVERSION:
                fields_rename.append(field_)
            else:
                fields_rename.append(model_str + "__" + field_)
        res_df = list2array(res_raw, fields_rename)
        if len(merge_df_tmp.columns) == 0:
            merge_df_tmp = res_df
        else:
            if res_df.shape[0] > 0:
                merge_df_tmp = pd.merge(merge_df_tmp, res_df, how='left', on=join_field)
            else:
                for field_ in fields_rename:
                    if field_ != join_field:
                        merge_df_tmp[field_] = [" " for row_ in range(merge_df_tmp.shape[0])]

            if join_field not in join_field_set:
                join_field_set.append(join_field)
            # Todo: 解决多个foreignkey
            columns_raw = list(merge_df_tmp.columns)
            not_join_field_set = []
            for column in columns_raw:
                if column not in join_field_set:
                    not_join_field_set.append(column)
            merge_df_tmp = merge_df_tmp[join_field_set + not_join_field_set].fillna(" ")
        len_models[model_str] = models_set[idx].objects.count()
    for ncol in range(merge_df_tmp.shape[1]):
        for nrow in range(merge_df_tmp.shape[0]):
            value_ = merge_df_tmp.iloc[nrow, ncol]
            if isinstance(value_, np.floating):
                value_ = round(value_, 3)
            elif isinstance(value_, np.integer) or isinstance(value_, str):
                value_ = value_
            merge_df_tmp.iloc[nrow, ncol] = value_
    json_files_tmp[time2] = os.path.join(MEDIA_ROOT, "json", '{}.{}.merge_df.json'.format(time2, apps[index]))
    merge_df_tmp.to_json(json_files_tmp[time2], date_format='iso')
    pd.DataFrame(len_models, index=[0]).to_json(os.path.join(MEDIA_ROOT, "json", '{}.{}.model_len.json'.format(
        time2, apps[index])))
    subprocess.run(["touch", done_file])
    subprocess.run(["rm", running_file])
    return True

