import datetime
import re
import os
from collections import defaultdict
import numpy as np
import pandas as pd
from django.forms.models import model_to_dict

from BIS.models import *
from LIMS.models import *
from SEQ.models import *
from ADVANCE.models import UploadFile
from databaseDemo.settings import MEDIA_ROOT


FILECOLUMN_TO_FIELD = {
    'normal': {
        'SampleInventoryInfo': {
            '患者编号': 'sampler_id',
            '血浆管数': 'plasma_num',
            '癌旁组织': 'adjacent_mucosa_num',
            '癌组织': 'cancer_tissue_num',
            '白细胞': 'WBC_num',
            '粪便': 'stool_num',
            '备注': 'memo',
        },
        'SampleInfo': {
            '样本编号': 'sample_id',
            '原始样本编号': 'raw_id',
            '冰箱位置': 'fridge',
            '孔板号': 'plate',
            '孔位': 'well',
            '样本类型': 'sample_type',
            '备注': 'memo',
        },
        'ExtractInfo': {
            '核酸提取编号': 'dna_id',
            '提取日期': 'extract_date',
            '样本类型': 'sample_type',
            '核酸类型': 'nucleic_type',
            '样本体积': 'sample_volume',
            '提取方法': 'extract_method',
            '浓度': 'dna_con',
            '体积': 'dna_vol',
            '冰箱位置': 'fridge',
            '孔板号': 'plate',
            '孔位': 'well',
            '核酸提取总量': 'totalM',
            '成功建库使用量': 'successM',
            '失败建库使用量': 'failM',
            '科研项目使用量': 'researchM',
            '其他使用量': 'othersM',
            '备注': 'memo'
        },
        'DNAUsageRecordInfo': {
            '使用日期': 'usage_date',
            '使用量': 'mass',
            '用途': 'usage',
            '建库编号(如有)': 'singleLB_id',
            '备注': 'memo'
        },
        'MethyLibraryInfo': {
            '建库编号': 'singleLB_id',
            '管上编号': 'tube_id',
            '是否临床': 'clinical_boolen',
            '文库名': 'singleLB_name',
            '样本标签': 'label',
            'index列表': 'barcodes',
            '建库日期': 'LB_date',
            '建库方法': 'LB_method',
            '试剂批次': 'kit_batch',
            '起始量': 'mass',
            'PCR循环数': 'pcr_cycles',
            '文库浓度': 'LB_con',
            '文库体积': 'LB_vol',
            '操作人': 'operator',
            '备注': 'memo'
        },
        'MethyCaptureInfo': {
            '捕获文库名': 'poolingLB_id',
            '杂交日期': 'hybrid_date',
            '杂交探针': 'probes',
            '杂交时间(min)': 'hybrid_min',
            'PostPCR循环数': 'postpcr_cycles',
            'PostPCR浓度': 'postpcr_con',
            '洗脱体积': 'elution_vol',
            '操作人': 'operator',
            '备注': 'memo'
        },
        'MethyPoolingInfo': {
            '测序文库名': 'singleLB_Pooling_id',
            'pooling比例': 'pooling_ratio',
            '取样': 'mass',
            '体积': 'volume',
            '备注': 'memo'
        },
        'SequencingInfo': {
            '上机文库号': 'sequencing_id',
            '送测日期': 'send_date',
            '上机时间': 'start_time',
            '下机时间': 'end_time',
            '机器号': 'machine_id',
            '芯片号': 'chip_id',
            '备注': 'memo'
        },
        'MethyQCInfo': {
            'Sample': 'QC_id',
            'Data_Size(Gb)': 'data_size_gb_field',
            'Clean_Rate(%)': 'clean_rate_field',
            'R1_Q20': 'r1_q20',
            'R2_Q20': 'r2_q20',
            'R1_Q30': 'r1_q30',
            'R2_Q30': 'r2_q30',
            'GC_Content': 'gc_content',
            'BS_conversion_rate(lambda_DNA)': 'bs_conversion_rate_lambda_dna_field',
            'BS_conversion_rate(CHH)': 'bs_conversion_rate_chh_field',
            'BS_conversion_rate(CHG)': 'bs_conversion_rate_chg_field',
            'Uniquely_Paired_Mapping_Rate': 'uniquely_paired_mapping_rate',
            'Mismatch_and_InDel_Rate': 'mismatch_and_indel_rate',
            'Mode_Fragment_Length(bp)': 'mode_fragment_length_bp_field',
            'Genome_Duplication_Rate': 'genome_duplication_rate',
            'Genome_Depth(X)': 'genome_depth_x_field',
            'Genome_Dedupped_Depth(X)': 'genome_dedupped_depth_x_field',
            'Genome_Coverage': 'genome_coverage',
            'Genome_4X_CpG_Depth(X)': 'genome_4x_cpg_depth_x_field',
            'Genome_4X_CpG_Coverage': 'genome_4x_cpg_coverage',
            'Genome_4X_CpG_methylation_level': 'genome_4x_cpg_methylation_level',
            'Panel_4X_CpG_Depth(X)': 'panel_4x_cpg_depth_x_field',
            'Panel_4X_CpG_Coverage': 'panel_4x_cpg_coverage',
            'Panel_4X_CpG_methylation_level': 'panel_4x_cpg_methylation_level',
            'Panel_Ontarget_Rate(region)': 'panel_ontarget_rate_region_field',
            'Panel_Duplication_Rate(region)': 'panel_duplication_rate_region_field',
            'Panel_Depth(site,X)': 'panel_depth_site_x_field',
            'Panel_Dedupped_Depth(site,X)': 'panel_dedupped_depth_site_x_field',
            'Panel_Coverage(site,1X)': 'panel_coverage_site_1x_field',
            'Panel_Coverage(site,10X)': 'panel_coverage_site_10x_field',
            'Panel_Coverage(site,20X)': 'panel_coverage_site_20x_field',
            'Panel_Coverage(site,50X)': 'panel_coverage_site_50x_field',
            'Panel_Coverage(site,100X)': 'panel_coverage_site_100x_field',
            'Panel_Uniformity(site,>20%mean)': 'panel_uniformity_site_20_mean_field',
            'Strand_balance(F)': 'strand_balance_f_field',
            'Strand_balance(R)': 'strand_balance_r_field',
            'GC_bin_depth_ratio': 'gc_bin_depth_ratio',
            '备注': 'memo'
        },
        'UploadFile': {
            '上传文件': 'uploadFile',
            '项目': 'uploadUrl',
            '上传者': 'uploadOperator',
            '上传时间': 'uploadTime'
        }
    },
    'foreign': {
        'SampleInfo': {
            '患者编号': 'sampler_id'
        },
        'ExtractInfo': {
            '样本编号': 'sample_id'
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
            '测序文库名': 'singleLB_Pooling_id',
            '上机文库号': 'sequencing_id'
        }
    },
    'foreignAdd': {
        'ExtractInfo': {
            '患者编号': [SampleInfo, 'sample_id', '样本编号', 'sampler_id']
        },
        'DNAUsageRecordInfo': {
            '患者编号': [ExtractInfo, 'dna_id', '核酸提取编号', 'sampler_id'],
            '样本编号': [ExtractInfo, 'dna_id', '核酸提取编号', 'sample_id']
        },
        'MethyLibraryInfo': {
            '患者编号': [ExtractInfo, 'dna_id', '核酸提取编号', 'sampler_id'],
            '样本编号': [ExtractInfo, 'dna_id', '核酸提取编号', 'sample_id']
        },
        'MethyPoolingInfo': {
            '患者编号': [MethyLibraryInfo, 'singleLB_id', '建库编号', 'sampler_id'],
            '样本编号': [MethyLibraryInfo, 'singleLB_id', '建库编号', 'sample_id'],
            '核酸提取编号': [MethyLibraryInfo, 'singleLB_id', '建库编号', 'dna_id']
        },
        'MethyQCInfo': {
            '患者编号': [MethyPoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'sampler_id'],
            '样本编号': [MethyPoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'sample_id'],
            '核酸提取编号': [MethyPoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'dna_id'],
            '建库编号': [MethyPoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'singleLB_id'],
            '捕获文库名': [MethyPoolingInfo, 'singleLB_Pooling_id', '测序文库名', 'poolingLB_id']
        }
    }
}

FOREIGNKEY_TO_MODEL = {
    'sampler_id': SampleInventoryInfo,
    'sample_id': SampleInfo,
    'dna_id': ExtractInfo,
    'singleLB_id': MethyLibraryInfo,
    'poolingLB_id': MethyCaptureInfo,
    'singleLB_Pooling_id': MethyPoolingInfo,
    'sequencing_id': SequencingInfo
}

KEY1_TO_MODEL = {
    'SampleInventoryInfo': SampleInventoryInfo,
    'SampleInfo': SampleInfo,
    'ExtractInfo': ExtractInfo,
    'DNAUsageRecordInfo': DNAUsageRecordInfo,
    'LibraryInfo': MethyLibraryInfo,
    'CaptureInfo': MethyCaptureInfo,
    'PoolingInfo': MethyPoolingInfo,
    'SequencingInfo': SequencingInfo,
    'QCInfo': MethyQCInfo
}

model_fields = {
    'SampleInventoryInfo': ['SampleInfo_SampleInventoryInfo', 'ExtractInfo_SampleInventoryInfo', 
                            'DNAUsageRecordInfo_SampleInventoryInfo', 'sampler_id', 'plasma_num', 
                            'adjacent_mucosa_num', 'cancer_tissue_num', 'WBC_num', 'stool_num', 'memo', 
                            'index', 'last_modify_time', 'create_time'],
    'SampleInfo': ['ExtractInfo_SampleInfo', 'DNAUsageRecordInfo_SampleInfo', 'sampler_id', 'sample_id', 'raw_id',
                   'fridge', 'plate', 'well', 'sample_type', 'memo', 'index', 'last_modify_time', 'create_time'],
    'ExtractInfo': ['DNAUsageRecordInfo_ExtractInfo', 'dna_id', 'sampler_id', 'sample_id', 'extract_date',
                    'sample_type', 'nucleic_type', 'sample_volume', 'extract_method', 'dna_con', 'dna_vol', 'fridge',
                    'plate', 'well', 'successM', 'failM', 'researchM', 'othersM', 'memo', 'index', 'last_modify_time', 
                    'create_time'],
    'DNAUsageRecordInfo': ['dna_id', 'sampler_id', 'sample_id', 'usage_date', 'mass', 'usage', 'singleLB_id', 'memo',
                           'index', 'last_modify_time', 'create_time'],
    'MethyLibraryInfo': ['MethyPoolingInfo_MethyLibraryInfo', 'singleLB_id', 'sampler_id', 'sample_id', 'dna_id', 'tube_id',
                         'clinical_boolen', 'singleLB_name', 'label', 'barcodes', 'LB_date', 'LB_method', 'kit_batch',
                         'mass', 'pcr_cycles', 'LB_con', 'LB_vol', 'operator', 'memo', 'index', 'last_modify_time',
                         'create_time'],
    'MethyCaptureInfo': ['MethyPoolingInfo_MethyCaptureInfo', 'poolingLB_id', 'hybrid_date', 'probes', 'hybrid_min',
                         'postpcr_cycles', 'postpcr_con', 'elution_vol', 'operator', 'memo', 'index',
                         'last_modify_time', 'create_time'],
    'MethyPoolingInfo': ['sampler_id', 'sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id','singleLB_Pooling_id',
                         'pooling_ratio', 'mass', 'volume', 'memo', 'index', 'last_modify_time', 'create_time'],
    'SequencingInfo': ['MethyQCInfo_SequencingInfo', 'sequencing_id', 'send_date', 'start_time', 'end_time',
                       'machine_id', 'chip_id', 'memo', 'index', 'last_modify_time', 'create_time', 'poolingLB_id'],
    'MethyQCInfo': ['QC_id', 'data_size_gb_field', 'clean_rate_field', 'r1_q20', 'r2_q20', 'r1_q30', 'r2_q30',
                    'gc_content', 'bs_conversion_rate_lambda_dna_field', 'bs_conversion_rate_chh_field',
                    'bs_conversion_rate_chg_field', 'uniquely_paired_mapping_rate', 'mismatch_and_indel_rate',
                    'mode_fragment_length_bp_field', 'genome_duplication_rate', 'genome_depth_x_field',
                    'genome_dedupped_depth_x_field', 'genome_coverage', 'genome_4x_cpg_depth_x_field',
                    'genome_4x_cpg_coverage', 'genome_4x_cpg_methylation_level', 'panel_4x_cpg_depth_x_field',
                    'panel_4x_cpg_coverage', 'panel_4x_cpg_methylation_level', 'panel_ontarget_rate_region_field',
                    'panel_duplication_rate_region_field', 'panel_depth_site_x_field',
                    'panel_dedupped_depth_site_x_field', 'panel_coverage_site_1x_field',
                    'panel_coverage_site_10x_field', 'panel_coverage_site_20x_field', 'panel_coverage_site_50x_field',
                    'panel_coverage_site_100x_field', 'panel_uniformity_site_20_mean_field', 'strand_balance_f_field',
                    'strand_balance_r_field', 'gc_bin_depth_ratio', 'sampler_id', 'sample_id', 'dna_id', 'singleLB_id',
                    'poolingLB_id', 'singleLB_Pooling_id', 'sequencing_id', 'memo', 'index', 'last_modify_time',
                    'create_time']

}

special_fields = ['sampler_id', 'sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id',
                  'sequencing_id']
model_links = {
    'SampleInventoryInfo': ['sampler_id'],
    'SampleInfo': ['sampler_id', 'sample_id'],
    'ExtractInfo': ['sampler_id', 'sample_id', 'dna_id'],
    'DNAUsageRecordInfo': ['sampler_id', 'sample_id', 'dna_id'],
    'DNAInventoryInfo': ['sampler_id', 'sample_id', 'dna_id'],
    'MethyLibraryInfo': ['sampler_id', 'sample_id', 'dna_id', 'singleLB_id'],
    'MethyCaptureInfo': ['poolingLB_id'],
    'MethyPoolingInfo': ['sampler_id', 'sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id'],
    'SequencingInfo': ['poolingLB_id', 'sequencing_id'],
    'MethyQCInfo': ['sampler_id', 'sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id',
                    'sequencing_id']
}
models_set = [SampleInventoryInfo, SampleInfo, ExtractInfo, DNAUsageRecordInfo, MethyLibraryInfo, MethyCaptureInfo,
              MethyPoolingInfo, SequencingInfo, MethyQCInfo]
models_set2 = ['SampleInventoryInfo', 'SampleInfo', 'ExtractInfo', 'DNAUsageRecordInfo', 'MethyLibraryInfo',
               'MethyCaptureInfo', 'MethyPoolingInfo', 'SequencingInfo', 'MethyQCInfo']


def clean_data(data_, warning_msg_dict, error_msg_dict, skip_list, emptyDrop_list, repeatDrop_list, str_list, num_list,
               date_list):
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
            data[id1] = [u'无' for x in range(data.shape[0])]
            if id1.rfind(u'备注') == -1:
                warning_msg_dict['empty'] = warning_msg_dict['empty'] + [u'第{}行"{}"列'.format(x + 2, id1) for x in
                                                                         range(data.shape[0])]
            continue

        col_data = []
        for id2 in range(len(data[id])):
            if pd.isnull(data[id1][id2]):
                col_data.append(u'无')
                if id1.rfind(u'备注') == -1:
                    warning_msg_dict['empty'].append(u'第{}行"{}"列'.format(id2 + 2, id1))
            else:
                col_data.append(data[id1][id2].strip())

        data[id1] = col_data

    for id1 in num_list:
        if id1 not in data:
            data[id1] = [9999 for x in range(data.shape[0])]
            warning_msg_dict['empty'] = warning_msg_dict['empty'] + [u'第{}行"{}"列'.format(x + 2, id1) for x in
                                                                     range(data.shape[0])]
            continue

        col_data = []
        for id2 in range(len(data[id1])):
            m1 = re.match(r'^(\d+)[^0-9]+$', str(data[id1][id2]).strip())
            m2 = re.match(r'^(\d+\.\d+)[^0-9]+$', str(data[id1][id2]).strip())
            # 判断数值为空
            if pd.isnull(data[id1][id2]) or str(data[id1][id2]).strip() == '-' or str(data[id1][id2]).strip() == '-%' \
                    or re.match(r'^-bp$', str(data[id1][id2]).strip(), flags=re.IGNORECASE):
                col_data.append(9999)
                warning_msg_dict['empty'].append(u'第{}行"{}"列'.format(id2 + 2, id1))
            elif pd.api.types.is_number(data[id1][id2]):
                col_data.append(data[id1][id2])
            elif re.match(r'^\d+$', str(data[id1][id2])) or re.match(r'^\d+\.0+$', str(data[id1][id2])):
                col_data.append(int(data[id1][id2]))
            elif re.match(r'^\d+\.\d+$', str(data[id1][id2])) or re.match(r'^-?\d[eE][+-]\d+$', str(data[id1][id2])):
                col_data.append(float(data[id1][id2]))
            elif m1:
                col_data.append(int(m1.group(1)))
            elif m2:
                col_data.append(float(m2.group(2)))
            else:
                col_data.append(9999)
                warning_msg_dict['invalid'].append(u'第{}行"{}"列'.format(id2 + 2, id1))
        data[id1] = col_data

    # data[id] = [0 if pd.isnull(x) else x for x in data[id]]
    for id1 in date_list:
        if id1 not in data:
            data[id1] = ['2000-01-01' for x in range(data.shape[0])]
            warning_msg_dict['empty'] = warning_msg_dict['empty'] + [u'第{}行"{}"列'.format(x + 2, id1) for x in
                                                                     range(data.shape[0])]
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
                    warning_msg_dict['empty'].append(u'第{}行"{}"列'.format(id2 + 2, id1))
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
        # print("id1: {}, col_data: {}".format(id1, col_data))
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
    # print(">>>>>>>>>> raw excel >>>>>>>>>>>>")
    # print(df)
    data = []
    skip_list = [0 for x in range(df.shape[0])]
    fatal_error = ""
    if url == 'SampleInventoryInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['SampleInventoryInfo'].keys())
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'患者编号'])] = []
            # clean_data(data_, warning_msg_dict, error_msg_dict, skip_list,
            #            emptyDrop_list, repeatDrop_list, str_list, num_list, date_list)
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'患者编号'],
                              [u'患者编号'],
                              [u'备注'],
                              [u'血浆管数', u'癌旁组织', u'癌组织', u'白细胞', '粪便'],
                              [])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'SampleInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['SampleInfo'].keys())
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'样本编号'])] = []
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'患者编号', u'样本编号'],
                              [u'样本编号'],
                              [u'冰箱位置', u'孔板号', u'孔位', u'样本类型', u'备注'],
                              [],
                              [])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'ExtractInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['ExtractInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['ExtractInfo'].keys())
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'核酸提取编号'])] = []
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'核酸提取编号', u'样本编号'],
                              [u'核酸提取编号'],
                              [u'样本类型', u'提取方法', u'冰箱位置', u'孔板号', u'孔位', u'样本类型', u'备注'],
                              [u'样本体积', u'浓度', u'体积', u'成功建库使用量', u'失败建库使用量', u'科研项目使用量',
                               u'其他使用量'],
                              [u'提取日期'])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'DNAUsageRecordInfo':
        df[u'建库编号(如有)'] = [u'无' for x in range(df.shape[0])]
        cols = list(FILECOLUMN_TO_FIELD['normal']['DNAUsageRecordInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['DNAUsageRecordInfo'].keys())
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'核酸提取编号', u'用途', u'使用日期'])] = []
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'核酸提取编号', u'用途', u'使用日期'],
                              [u'核酸提取编号', u'用途', u'使用日期'],
                              [u'用途', u'建库编号(如有)', u'备注'],
                              [u'使用量'],
                              [u'使用日期'])
            for row in range(len(df[u'用途'])):
                if df[u'用途'][row] not in [u'建库失败', u'科研项目', u'其他']:
                    skip_list[row] = 1
                    error_msg_dict['emptyKey'][u'用途'] = [u'第{}行'.format(row + 2)]
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'MethyLibraryInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['MethyLibraryInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['MethyLibraryInfo'].keys())
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'建库编号'])] = []
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'核酸提取编号', u'建库编号'],
                              [u'建库编号'],
                              [u'管上编号', u'是否临床', u'文库名', u'样本标签', u'index列表',
                               u'建库方法', u'试剂批次', u'操作人', u'备注'],
                              [u'起始量', u'PCR循环数', u'文库浓度', u'文库体积'],
                              [u'建库日期'])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'MethyCaptureInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['MethyCaptureInfo'].keys())
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'捕获文库名'])] = []
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'捕获文库名'],
                              [u'捕获文库名'],
                              [u'杂交探针', u'操作人', u'备注'],
                              [u'杂交时间(min)', u'PostPCR循环数', u'PostPCR浓度', u'洗脱体积'],
                              [u'杂交日期'])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'MethyPoolingInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['MethyPoolingInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['MethyPoolingInfo'].keys())
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'测序文库名'])] = []
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'建库编号', u'捕获文库名', u'测序文库名'],
                              [u'测序文库名'],
                              [u'备注'],
                              [u'pooling比例', u'取样', u'体积'],
                              [])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'SequencingInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['SequencingInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['SequencingInfo'].keys())
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'上机文库号'])] = []
            data[u'捕获文库名'] = [[y.strip() for y in x.split(',')] for x in data[u'捕获文库名']]
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'捕获文库名', u'上机文库号'],
                              [u'上机文库号'],
                              [u'机器号', u'芯片号', u'备注'],
                              [],
                              [u'送测日期', u'上机时间', u'下机时间'])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'MethyQCInfo':
        cols = list(FILECOLUMN_TO_FIELD['normal']['MethyQCInfo'].keys()) + \
               list(FILECOLUMN_TO_FIELD['foreign']['MethyQCInfo'].keys())
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'Sample'])] = []
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'测序文库名', u'上机文库号', u'Sample'],
                              [u'Sample'],
                              [u'备注'],
                              [u'Data_Size(Gb)', u'Clean_Rate(%)', u'R1_Q20', u'R2_Q20', u'R1_Q30', u'R2_Q30',
                               u'GC_Content', u'BS_conversion_rate(lambda_DNA)', u'BS_conversion_rate(CHH)',
                               u'BS_conversion_rate(CHG)', u'Uniquely_Paired_Mapping_Rate', u'Mismatch_and_InDel_Rate',
                               u'Mode_Fragment_Length(bp)', u'Genome_Duplication_Rate', u'Genome_Depth(X)',
                               u'Genome_Dedupped_Depth(X)', u'Genome_Coverage', u'Genome_4X_CpG_Depth(X)',
                               u'Genome_4X_CpG_Coverage', u'Genome_4X_CpG_methylation_level', u'Panel_4X_CpG_Depth(X)',
                               u'Panel_4X_CpG_Coverage', u'Panel_4X_CpG_methylation_level',
                               u'Panel_Ontarget_Rate(region)',
                               u'Panel_Duplication_Rate(region)', u'Panel_Depth(site,X)',
                               u'Panel_Dedupped_Depth(site,X)',
                               u'Panel_Coverage(site,1X)', u'Panel_Coverage(site,10X)', u'Panel_Coverage(site,20X)',
                               u'Panel_Coverage(site,50X)', u'Panel_Coverage(site,100X)',
                               u'Panel_Uniformity(site,>20%mean)', u'Strand_balance(F)', u'Strand_balance(R)',
                               u'GC_bin_depth_ratio'],
                              [])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    elif url == 'MethyCaptureInfoPlus':
        cols = list(set(list(FILECOLUMN_TO_FIELD['normal']['MethyCaptureInfo'].keys()) +
                        list(FILECOLUMN_TO_FIELD['normal']['MethyPoolingInfo'].keys()) +
                        list(FILECOLUMN_TO_FIELD['foreign']['MethyPoolingInfo'].keys())))
        try:
            data = df[cols].copy(deep=True)
            error_msg_dict['repeatKey']['/ '.join([u'建库编号', u'捕获文库名', u'测序文库名'])] = []
            data = clean_data(data, warning_msg_dict, error_msg_dict, skip_list,
                              [u'建库编号', u'捕获文库名', u'测序文库名'],
                              [u'建库编号', u'捕获文库名', u'测序文库名'],
                              [u'杂交探针', u'操作人', u'备注'],
                              [u'杂交时间(min)', u'PostPCR循环数', u'PostPCR浓度',
                               u'洗脱体积', u'pooling比例', u'取样', u'体积'],
                              [u'杂交日期'])
        except KeyError:
            fatal_error = "严重错误！！！输入表格未包含需要的字段，请下载正确的excel模板。"
            return data, skip_list, fatal_error
    # print("return data:\n>>>>>>>")
    # pprint(data)
    # print("<<<<<<<<<")
    return data, skip_list, fatal_error


def save_records(upload_file):
    warning_msg = ""
    warning_msg_dict = defaultdict(list)
    # warning_msg_dict = {
    # 	'empty': [],
    # 	'invalid': []
    # }
    error_msg = ""
    error_msg_dict = defaultdict(dict)
    # error_msg_dict = {
    # 	'repeatKey': [],
    # 	'noForeignKey': {},
    # 	'emptyKey': {}
    # }
    # 读取文件，进行数据清洗
    records, skip_list, fatal_error = read_file(
        upload_file.uploadUrl, upload_file.uploadFile.path, warning_msg_dict, error_msg_dict)

    if fatal_error:
        return 'NA', 'NA', 'NA', '', '', fatal_error

    addlist = []
    context_pre = {}
    for row in range(records.shape[0]):
        if skip_list[row]:
            # print("skip row {} from skip_list".format(row))
            # print(skip_list)
            continue
        context = {}
        created = False
        next_bool = False
        if upload_file.uploadUrl in FILECOLUMN_TO_FIELD['normal']:
            # 数据预处理
            if upload_file.uploadUrl in FILECOLUMN_TO_FIELD['foreign']:
                for col in FILECOLUMN_TO_FIELD['foreign'][upload_file.uploadUrl]:
                    model_key = FILECOLUMN_TO_FIELD['foreign'][upload_file.uploadUrl][col]
                    # 获取foreignKey对应的object
                    # print('upload_file.uploadUrl: %s; model_key: %s' % (upload_file.uploadUrl, model_key))
                    if not (upload_file.uploadUrl == 'SequencingInfo' and model_key == 'poolingLB_id'):
                        # print('model: {}; key: {}; value: {}'.format(FOREIGNKEY_TO_MODEL[model_key], model_key,
                        # records[col][row]))
                        try:
                            obj_ = FOREIGNKEY_TO_MODEL[model_key].objects.get(
                                **{model_key: records[col][row]})
                            # print(obj_)
                            context[model_key] = obj_
                        except FOREIGNKEY_TO_MODEL[model_key].DoesNotExist:
                            if col in error_msg_dict:
                                error_msg_dict['noForeignKey'][col].append(u'第{}行'.format(row + 2))
                            else:
                                error_msg_dict['noForeignKey'][col] = [u'第{}行'.format(row + 2)]
                            # print("change skip_list[{}] to 1".format(row))
                            skip_list[row] = 1
                            next_bool = True
                            break

            for col in FILECOLUMN_TO_FIELD['normal'][upload_file.uploadUrl]:
                context[FILECOLUMN_TO_FIELD['normal'][upload_file.uploadUrl][col]] = records[col][row]

            if next_bool:
                # print("skip row {} from next_bool".format(row))
                # print(skip_list)
                continue

            if upload_file.uploadUrl in FILECOLUMN_TO_FIELD['foreignAdd']:
                # 对于输入文件中缺少的外键k1，
                # 先找到输入文件中存在的外键k2，
                # 再通过k2对应的model2找到k1对应的值value1
                # 再通过k1对应的model1找到相应对象
                for col in FILECOLUMN_TO_FIELD['foreignAdd'][upload_file.uploadUrl]:
                    l_ = FILECOLUMN_TO_FIELD['foreignAdd'][upload_file.uploadUrl][col]
                    value = model_to_dict(l_[0].objects.get(
                        **{l_[1]: records[l_[2]][row]}))[l_[3]]
                    obj_ = FOREIGNKEY_TO_MODEL[l_[3]].objects.get(**{l_[3]: value})
                    context[l_[3]] = obj_

            # 模型增/改
            if upload_file.uploadUrl == 'SampleInfo':
                # 修改临床信息表
                _, created = SampleInfo.objects.update_or_create(
                    sample_id=records[u'样本编号'][row], defaults={**context})

            elif upload_file.uploadUrl == 'ExtractInfo':
                # 修改提取表
                _, created = ExtractInfo.objects.update_or_create(
                    dna_id=records[u'核酸提取编号'][row], defaults={**context})

            elif upload_file.uploadUrl == 'DNAUsageRecordInfo':
                # 修改库存表
                inventory = ExtractInfo.objects.get(
                    dna_id=context['dna_id'])
                try:  # PUT，改
                    usageRecord = DNAUsageRecordInfo.objects.get(
                        dna_id=context['dna_id'],
                        usage_date=records[u'使用日期'][row],
                        usage=records[u'用途'][row]
                    )
                    mass_ = float(records[u'使用量'][row]) - usageRecord.mass
                except DNAUsageRecordInfo.DoesNotExist:  # POST，增
                    mass_ = float(records[u'使用量'][row])
                if records[u'用途'][row] == '建库失败':
                    inventory.failM = inventory.failM + mass_
                elif records[u'用途'][row] == '科研项目':
                    inventory.researchM = inventory.researchM + mass_
                elif records[u'用途'][row] == '其他':
                    inventory.othersM = inventory.othersM + mass_
                inventory.save()
                # 修改使用记录表
                _, created = DNAUsageRecordInfo.objects.update_or_create(
                    dna_id=context['dna_id'],
                    usage_date=records[u'使用日期'][row],
                    usage=records[u'用途'][row],
                    defaults={**context})

            elif upload_file.uploadUrl == 'MethyLibraryInfo':
                _, created = MethyLibraryInfo.objects.update_or_create(
                    singleLB_id=records[u'建库编号'][row], defaults={**context})
                # 修改使用记录表
                try:  # PUT，改
                    usageRecord = DNAUsageRecordInfo.objects.get(
                        dna_id=context['dna_id'],
                        usage_date=records[u'建库日期'][row],
                        usage='建库成功'
                    )
                    sub_ = float(records[u'起始量'][row]) - usageRecord.mass
                    usageRecord.mass = usageRecord.mass + sub_
                    usageRecord.save()
                    mass_inventory = sub_
                except DNAUsageRecordInfo.DoesNotExist:  # POST，增
                    context2 = {
                        'sample_id': context['sample_id'], 'dna_id': context['dna_id'],
                        'usage_date': records[u'建库日期'][row], 'mass': records[u'起始量'][row],
                        'usage': '建库成功', 'singleLB_id': records[u'建库编号'][row],
                        'memo': records[u'备注'][row]
                    }
                    usageRecord = DNAUsageRecordInfo(**context2)
                    usageRecord.save()
                    mass_inventory = float(records[u'起始量'][row])
                # 修改库存表
                inventory = ExtractInfo.objects.get(dna_id=context['dna_id'])
                inventory.successM = inventory.successM + mass_inventory
                inventory.save()

            elif upload_file.uploadUrl == 'MethyCaptureInfo':
                _, created = MethyCaptureInfo.objects.update_or_create(
                    poolingLB_id=records[u'捕获文库名'][row], defaults={**context})

            elif upload_file.uploadUrl == 'MethyPoolingInfo':
                _, created = MethyPoolingInfo.objects.update_or_create(
                    singleLB_Pooling_id=records[u'测序文库名'][row], defaults={**context})

            elif upload_file.uploadUrl == 'SequencingInfo':
                captures = []
                # print('>>>>>>>>>> notice >>>>>>>')
                # pprint(context)
                for c in records[u'捕获文库名'][row]:
                    try:
                        captures.append(
                            MethyCaptureInfo.objects.get(poolingLB_id=c))
                    except MethyCaptureInfo.DoesNotExist:
                        warning_msg_dict['empty'].append(
                            u'第{}行"{}"列的"{}"'.format(row + 2, u'捕获文库名', c))
                try:
                    # print('>>>>>>>>>> notice >>>>>>> update')
                    sequencing = SequencingInfo.objects.get(
                        sequencing_id=records[u'上机文库号'][row])
                    sequencing.__dict__.update(**context)
                    sequencing.poolingLB_id.add(*captures)
                except SequencingInfo.DoesNotExist:
                    # print('>>>>>>>>>> notice >>>>>>> create')
                    created = True
                    sequencing = SequencingInfo(**context)
                    sequencing.save()
                    sequencing.poolingLB_id.add(*captures)

            elif upload_file.uploadUrl == 'MethyQCInfo':
                _, created = MethyQCInfo.objects.update_or_create(
                    QC_id=records[u'Sample'][row], defaults={**context})

            if created:
                addlist.append(row)
        else:
            if upload_file.uploadUrl == 'MethyCaptureInfoPlus':
                for m in ['MethyCaptureInfo', 'MethyPoolingInfo']:
                    # 数据预处理
                    context = {}
                    if m in FILECOLUMN_TO_FIELD['foreign']:
                        for col in FILECOLUMN_TO_FIELD['foreign'][m]:
                            model_key = FILECOLUMN_TO_FIELD['foreign'][m][col]
                            # 获取foreignKey对应的object
                            # print(">>>>>>>>>>>>>> notice >>>>>>>>>>>")
                            # pprint({model_key: records[col][row]})
                            try:
                                obj_ = FOREIGNKEY_TO_MODEL[model_key].objects.get(
                                    **{model_key: records[col][row]})
                                context[model_key] = obj_
                            except FOREIGNKEY_TO_MODEL[model_key].DoesNotExist:
                                if col in error_msg_dict:
                                    error_msg_dict['noForeignKey'][col].append(u'第{}行'.format(row + 2))
                                else:
                                    error_msg_dict['noForeignKey'][col] = [u'第{}行'.format(row + 2)]
                                skip_list[row] = 1
                                next_bool = True
                                break
                    if next_bool:
                        break

                    for col in FILECOLUMN_TO_FIELD['normal'][m]:
                        context[FILECOLUMN_TO_FIELD['normal'][m][col]] = records[col][row]

                    if m in FILECOLUMN_TO_FIELD['foreignAdd']:
                        for col in FILECOLUMN_TO_FIELD['foreignAdd'][m]:
                            l_ = FILECOLUMN_TO_FIELD['foreignAdd'][m][col]
                            value = model_to_dict(l_[0].objects.get(
                                **{l_[1]: records[l_[2]][row]}))[l_[3]]
                            obj_ = FOREIGNKEY_TO_MODEL[l_[3]].objects.get(
                                **{l_[3]: value})
                            context[l_[3]] = obj_
                    # 模型增/改
                    # print(">>>>>>>>>>>>> notice >>>>>>>>>>>")
                    # pprint(context)
                    if m == 'MethyCaptureInfo':
                        # print(">>>>>>>>>>>>> notice >>>>>>>>>>>", records[u'捕获文库名'][row])
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
                    addlist.append(row)

    # print(skip_list)
    # print(">>>>>>>>>> cleaned data >>>>>>>>>>>>")
    # print(records)
    # pprint(warning_msg_dict)
    # pprint(error_msg_dict)
    # print(len(error_msg_dict['repeatKey'][list(error_msg_dict['repeatKey'].keys())[0]]))
    total = len(skip_list)
    valid = total - len([x for x in skip_list if x])
    # 输出 warning_msg, error_msg
    if len(warning_msg_dict['empty']) > 0:
        warning_msg += u'单元格为空或单元格值不存在：' + ', '.join(warning_msg_dict['empty'])
    if len(warning_msg_dict['invalid']) > 0:
        warning_msg += u'\n单元格值不符合格式：' + ', '.join(warning_msg_dict['invalid'])
    if len(error_msg_dict['repeatKey'][list(error_msg_dict['repeatKey'].keys())[0]]) > 0:
        error_msg += u'存在重复关键字段的行：' + ', '.join(['{}({})'.format(key, ', '.join(
            error_msg_dict['repeatKey'][key])) for key in error_msg_dict['repeatKey']])
    if len(error_msg_dict['emptyKey'].keys()) > 0:
        error_msg += u'\n关键字段缺失或不正确：' + ', '.join(['{}({})'.format(key, ', '.join(
            error_msg_dict['emptyKey'][key])) for key in error_msg_dict['emptyKey']])
    if len(error_msg_dict['noForeignKey'].keys()) > 0:
        error_msg += u'\n关联对象不存在：' + ', '.join(['{}({})'.format(key, ', '.join(
            error_msg_dict['noForeignKey'][key])) for key in error_msg_dict['noForeignKey']])
    # print("total: %s, len(addlist): %s" % (total, len(addlist)))
    return total, valid, len(addlist), warning_msg, error_msg, fatal_error


def list2array(list_, names):
    array = []
    for i in list_:
        array.append(list(i))
    return pd.DataFrame(array, columns=names)


def check_new_merge_df_all():
    flag_update = []
    json_files = []
    time2 = []
    time2_df_json = []
    time2_total = 0
    time2_total_df_json = ''
    m_lists = [[0, 1, 2, 3], [4, 5, 6], [7, 8]]
    for m_list in m_lists:
        tmp = check_new_merge_df(m_list)
        if tmp[0]:
            flag_update.append(tmp[0])
            json_files.append(tmp[1])
            time2.append(tmp[2])
            time2_df_json.append(tmp[3])

    for file in os.listdir(os.path.join(MEDIA_ROOT, "json")):
        if re.match(r'[0-9]+.*total\.merge_df.json', file):
            time2_tmp = file.split('.')[0]
            time2_tmp = int(time2_tmp)
            tmp_json = os.path.join(MEDIA_ROOT, "json", file)
            if time2_tmp > time2_total:
                time2_total = time2_tmp
                time2_total_df_json = tmp_json
    return flag_update, json_files, time2, time2_df_json, time2_total_df_json


def check_new_merge_df(m_list, name):
    json_files = {}
    time2 = 0
    time2_df_json = ""
    time2_len = {}
    for file in os.listdir(os.path.join(MEDIA_ROOT, "json")):
        if re.match(r'[0-9]+.*' + name + r'\.merge_df.json', file):
            time2_tmp = file.split('.')[0]
            time2_tmp = int(time2_tmp)
            json_files[time2_tmp] = os.path.join(MEDIA_ROOT, "json", file)
            if time2_tmp > time2:
                time2 = time2_tmp
                time2_df_json = json_files[time2_tmp]
                time2_len = pd.read_json(os.path.join(MEDIA_ROOT, "json", re.sub(r'\.merge_df\.', '.model_len.', file))
                                         ).to_dict(orient='records')[0]

    lastTime_models = {}
    len_models = {}
    for m in [0, 1, 2, 3, 4, 6, 5, 7, 8]: # m_list
        lastTime_models[models_set2[m]] = int(models_set[m].objects.values_list("last_modify_time").distinct().order_by(
            "-last_modify_time")[0][0].strftime("%Y%m%d%H%M%S%f"))
        len_models[models_set2[m]] = models_set[m].objects.count()
    flag_update = False
    # print("len_models: ")
    # print(len_models)
    # print("time2_len: ")
    # print(time2_len)
    # print("lastTime_models: ")
    # print(lastTime_models)
    # print("before time2: {}; flag_update: {}".format(time2, flag_update))
    for m in lastTime_models:
        # print("lastTime_models[m]:{}, time2:{}, m:{}, time2_len[m]:{}, len_models[m]:{}".format(lastTime_models[m],
        #                                                                                         time2, m,
        #                                                                                         time2_len[m],
        #                                                                                         len_models[m]))
        if lastTime_models[m] > time2:
            flag_update = True
            time2 = lastTime_models[m]
            # print("do replacement")
            break
        if m not in time2_len or time2_len[m] != len_models[m]:
            flag_update = True
            # print("do replacement")
            break
    # print("after time2: {}; flag_update: {}".format(time2, flag_update))
    return flag_update, json_files, time2, time2_df_json


def make_new_merge_df_all(json_files_tmp, time2):
    pass


def make_new_merge_df(json_files_tmp, time2):
    merge_df_tmp = []
    len_models = {}
    for m in [0, 1, 2, 3, 4, 6, 5, 7, 8]:
        if m == 0:
            fields = model_fields[models_set2[m]]
            fields_filt = fields[6:25]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['sample_id'] else 'SampleInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            merge_df_tmp = res_df
            len_models[models_set2[m]] = models_set[m].objects.count()
        elif m == 1:
            fields = model_fields[models_set2[m]]
            fields_filt = fields[5:14]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['sample_id', 'dna_id'] else 'ExtractInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            columns_raw = list(merge_df_tmp.columns)
            merge_df_tmp = pd.merge(merge_df_tmp, res_df, how='left', on='sample_id')
            merge_df_tmp = merge_df_tmp[['sample_id', 'dna_id'] + columns_raw[1:] + fields_filt_rename[2:]]
            len_models[models_set2[m]] = models_set[m].objects.count()
        elif m == 2:
            fields = model_fields[models_set2[m]]
            fields_filt = [fields[0]] + fields[2:7]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['dna_id'] else 'DNAUsageRecordInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            merge_df_tmp = pd.merge(merge_df_tmp, res_df, how='left', on='dna_id')
            len_models[models_set2[m]] = models_set[m].objects.count()
        elif m == 3:
            fields = model_fields[models_set2[m]]
            fields_filt = fields[1:7]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            res_raw_shift = []
            for l_ in res_raw:
                res_raw_shift.append(list(l_) + [round(l_[1] - l_[2] - l_[3] - l_[4] - l_[5], 3)])
            fields_filt_rename = [x if x in ['dna_id'] else 'DNAInventoryInfo_' + x for x in
                                  fields_filt + ['remainM']]
            res_df = list2array(res_raw_shift, fields_filt_rename)
            merge_df_tmp = pd.merge(merge_df_tmp, res_df, how='left', on='dna_id')
            len_models[models_set2[m]] = models_set[m].objects.count()
        elif m == 4:
            fields = model_fields[models_set2[m]]
            fields_filt = [fields[2]] + fields[5:19]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['dna_id', 'singleLB_id'] else 'LibraryInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            columns_raw = list(merge_df_tmp.columns)
            merge_df_tmp = pd.merge(merge_df_tmp, res_df, how='left', left_on='DNAUsageRecordInfo_singleLB_id',
                                    right_on='singleLB_id')
            merge_df_tmp['singleLB_id'] = merge_df_tmp['DNAUsageRecordInfo_singleLB_id']
            merge_df_tmp = merge_df_tmp[
                ['sample_id', 'dna_id', 'singleLB_id'] + columns_raw[2:] + fields_filt_rename[1:]]
            len_models[models_set2[m]] = models_set[m].objects.count()
        elif m == 6:
            fields = model_fields[models_set2[m]]
            fields_filt = fields[3:10]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id'] else
                                  'PoolingInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            columns_raw = list(merge_df_tmp.columns)
            merge_df_tmp = pd.merge(merge_df_tmp, res_df, how='left', on='singleLB_id')
            merge_df_tmp = merge_df_tmp[['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id'] +
                                        columns_raw[3:] + fields_filt_rename[3:]]
            len_models[models_set2[m]] = models_set[m].objects.count()
        elif m == 5:
            fields = model_fields[models_set2[m]]
            fields_filt = fields[3:13]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['poolingLB_id'] else 'CaptureInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            columns_raw = list(merge_df_tmp.columns)
            idx_ = columns_raw.index('PoolingInfo_pooling_ratio')
            merge_df_tmp = pd.merge(merge_df_tmp, res_df, how='left', on='poolingLB_id')
            merge_df_tmp = merge_df_tmp[columns_raw[:idx_] + fields_filt_rename[1:] + columns_raw[idx_:]]
            len_models[models_set2[m]] = models_set[m].objects.count()
        elif m == 7:
            fields = model_fields[models_set2[m]]
            fields_filt = [fields[11]] + fields[1:8]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            res_raw_shift = []
            for l_ in res_raw:
                if l_[0] is None:
                    continue
                elif isinstance(l_[0], int):
                    res_raw_shift.append(list(l_))
                elif isinstance(l_[0], list):
                    for idx in l_[0]:
                        res_raw_shift.append([idx] + list(l_[1:]))
            fields_filt_rename = [x if x in ['sequencing_id'] else 'SequencingInfo_' + x for x in fields_filt]
            res_df = list2array(res_raw_shift, fields_filt_rename)
            columns_raw = list(merge_df_tmp.columns)
            idx_ = columns_raw.index('CaptureInfo_index')
            merge_df_tmp = pd.merge(merge_df_tmp, res_df, how='left', left_on='CaptureInfo_index',
                                    right_on='SequencingInfo_poolingLB_id')
            merge_df_tmp = merge_df_tmp[
                special_fields + columns_raw[5:idx_] + columns_raw[idx_ + 1:] + fields_filt_rename[2:]]
            len_models[models_set2[m]] = models_set[m].objects.count()
        elif m == 8:
            fields = model_fields[models_set2[m]]
            fields_filt = fields[:44]
            res_raw = list(models_set[m].objects.values_list(*fields_filt))
            fields_filt_rename = [x if x in ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id',
                                             'singleLB_Pooling_id', 'sequencing_id'] else 'QCInfo_' +
                                                                                          x for x in fields_filt]
            res_df = list2array(res_raw, fields_filt_rename)
            merge_df_tmp = pd.merge(merge_df_tmp, res_df, how='left', on=special_fields)
            len_models[models_set2[m]] = models_set[m].objects.count()
    for link in special_fields:
        merge_df_tmp.loc[:, link].fillna(" ", inplace=True)
    for ncol in range(6, merge_df_tmp.shape[1]):
        for nrow in range(merge_df_tmp.shape[0]):
            value_ = merge_df_tmp.iloc[nrow, ncol]
            if pd.isna(value_):
                value_ = " "
            elif isinstance(value_, np.floating):
                value_ = round(value_, 3)
            elif isinstance(value_, np.integer) or isinstance(value_, str):
                value_ = value_
            merge_df_tmp.iloc[nrow, ncol] = value_
    merge_df_tmp.to_json(os.path.join(MEDIA_ROOT, "json", '{}.merge_df.json'.format(time2)), date_format='iso')
    pd.DataFrame(len_models, index=[0]).to_json(os.path.join(MEDIA_ROOT, "json", '{}.model_len.json'.format(time2)))
    if len(json_files_tmp.keys()) > 9:
        time2_tmp_list = sorted(list(json_files_tmp.keys()), reverse=True)
        for idx in range(9, len(time2_tmp_list)):
            os.remove(json_files_tmp[time2_tmp_list[idx]])
            os.remove(re.sub(r'\.merge_df\.', '.model_len.', json_files_tmp[time2_tmp_list[idx]]))
    print("merge_df_tmp is rebuild")
