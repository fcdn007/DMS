import datetime
import os
import re
import time

import pandas as pd
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import FieldError
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from USER.models import UserInfo, DatabaseRecord
from databaseDemo.settings import BASE_DIR, MEDIA_ROOT
from databaseDemo.tasks import make_new_merge_df_by_celery
from util.merge_df import model_links, models_set2
from util.merge_df import save_records, check_new_merge_df_all, FOREIGNKEY_TO_MODEL, KEY1_TO_MODEL, special_fields
from util.utils import read_file_by_stream, condition_filter
from .forms import FileUploadModelForm


# Create your views here.
def uniqueV(request):
    foreign_keys = {
        'SampleInfo': ['sampler_id'],
        'ExtractInfo': ['sampler_id', 'sample_id'],
        'DNAUsageRecordInfo': ['sampler_id', 'sample_id', 'dna_id'],
        'MethyLibraryInfo': ['sampler_id', 'sample_id', 'dna_id'],
        'MethyPoolingInfo': ['sampler_id', 'sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id'],
        'SequencingInfo': ['poolingLB_id'],
        'MethyQCInfo': ['sampler_id', 'sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id',
                        'sequencing_id'],
        'ClinicalInfo': ['sampler_id'],
        'FollowupInfo': ['sampler_id', 'Clinical_id'],
        'LiverPathologicalInfo': ['sampler_id', 'Clinical_id'],
        'LiverTMDInfo': ['sampler_id', 'Clinical_id'],
        'LiverBiochemInfo': ['sampler_id', 'Clinical_id']
    }
    query_fields = {
        'SampleInfo': ["sample_id", "name", "gender", "patientId", "category", "stage", "diagnose", "diagnose_others",
                       "centrifugation_date", "hospital", "department", "send_date", "memo"],
        'ExtractInfo': ['sample_id', 'dna_id', 'extract_date', 'sample_type', 'extract_method', 'memo'],
        'DNAUsageRecordInfo': ['sample_id', 'dna_id', 'usage_date', 'singleLB_id', 'memo'],
        'DNAInventoryInfo': ['sample_id', 'dna_id'],
        'LibraryInfo': ['sample_id', 'dna_id', 'singleLB_id', 'tube_id', 'clinical_boolen', 'singleLB_name', 'label',
                        'barcodes', 'LB_date', 'LB_method', 'kit_batch', 'operator', 'memo'],
        'CaptureInfo': ['poolingLB_id', 'hybrid_date', 'probes', 'operator', 'memo'],
        'PoolingInfo': ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id', 'memo'],
        'SequencingInfo': ['poolingLB_id', 'sequencing_id', 'send_date', 'start_time', 'end_time', 'machine_id',
                           'chip_id', 'memo'],
        'QCInfo': ['sample_id', 'dna_id', 'singleLB_id', 'poolingLB_id', 'singleLB_Pooling_id', 'sequencing_id',
                   'memo']
    }
    data = {}
    key1 = request.GET['model']
    key2 = request.GET['filed']
    if key1 in query_fields and key2 in query_fields[key1]:
        if key1 in foreign_keys and key2 in foreign_keys[key1]:
            data['values'] = [x[0] for x in
                              FOREIGNKEY_TO_MODEL[key2].objects.values_list(key2).distinct().order_by(key2)]
        else:
            data['values'] = [x[0] for x in
                              KEY1_TO_MODEL[key1].objects.values_list(key2).distinct().order_by(key2)]

    else:
        data['values'] = []
    return JsonResponse(data)

@csrf_exempt
def uploadV(request):
    # pprint(request)
    if request.method == "POST":
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        user = UserInfo.objects.get(username=request.user.username)
        # print("form: %s" % form)

        if form.is_valid():
            # print("form.is_valid(): TRUE")
            upload_file = form.save()
            # print('upload_file.uploadUrl: %s' % upload_file.uploadUrl)
            # print('upload_file.uploadOperator: %s' % upload_file.uploadOperator)
            # print('upload_file.uploadFile: %s' % upload_file.uploadFile)
            # print(upload_file.uploadFile.path)
            # read file and add records to model
            total, valid, add, warning, error_msg, fatal_error = save_records(upload_file)
            if fatal_error:
                context2 = {
                    'userinfo': user, 'model_changed': request.POST.get('uploadUrl'),
                    'operation': "批量上传失败",
                    'memo': "file_path: {};fatal_error: {}".format(upload_file.uploadFile.path, fatal_error)
                }
                record_obj = DatabaseRecord(**context2)
                record_obj.save()
                return JsonResponse({
                    'error_msg_fatal': fatal_error
                })
            else:
                context2 = {
                    'userinfo': user, 'model_changed': request.POST.get('uploadUrl'),
                    'operation': "批量上传成功",
                    'memo': "file_path: {};all_records: {};valid_records: {};error_msg_tolerant: {}".format(
                        upload_file.uploadFile.path, total, valid, error_msg)
                }
                record_obj = DatabaseRecord(**context2)
                record_obj.save()
                return JsonResponse({
                    'all_records': total, 'valid_records': valid, 'add_records': add, 'warning': warning,
                    'error_msg_tolerant': error_msg
                })
        else:
            # print("form.is_valid(): FALSE")
            data = {'error_msg_fatal': "严重错误！！！文件上传和批量添加失败。只允许上传以下格式文件：txt, csv and xlsx。"}
            context2 = {
                'userinfo': user, 'model_changed': request.POST.get('uploadUrl'),
                'operation': "批量上传文件格式错误",
                'memo': "无"
            }
            record_obj = DatabaseRecord(**context2)
            record_obj.save()
            return JsonResponse(data)
    return JsonResponse({'error_msg_fatal': '严重错误！！！只接受POST请求。'})


@login_required
@never_cache
def AdvanceUploadV(request):
    return render(request, 'ADVANCE/AdvancedUpload.html')


@login_required
@csrf_exempt
@permission_required('ADVANCE.access_Advance')
def AdvancedSearchV(request):
    # 合并所有model，形成一张大表
    # 检测所有model的最新修改时间time1，
    # > 如果time1等于已有json文件的时间戳time2，直接读取已有的json文件，
    # > 否则重新创建merge_df，并把merge_df输出为json文件，打上时间戳。清除旧的json文件(保留10个)
    merge_df = []
    flag_update, json_files, time2, time2_json, time2_total_json = check_new_merge_df_all()
    if len(flag_update) > 0:
        # 使用djcelery异步执行make_new_merge_df
        print("do make_new_merge_df_by_celery")
        make_new_merge_df_by_celery.delay(json_files, time2)
    else:
        merge_df = pd.read_json(time2_total_json)
        for col_ in ['ClinicalInfo_centrifugation_date', 'ClinicalInfo_send_date', 'ExtractInfo_extract_date',
                     'DNAUsageRecordInfo_usage_date', 'LibraryInfo_LB_date', 'CaptureInfo_hybrid_date',
                     'SequencingInfo_send_date', 'SequencingInfo_start_time', 'SequencingInfo_end_time']:
            merge_df.loc[:, col_] = [datetime.datetime.strptime(date_, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                                     if re.match(r'\d+-\d+-\d+T\d+:\d+:\d+\.\d+Z', date_)
                                     else datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date() for date_ in
                                     merge_df.loc[:, col_]]
        print("read merge_df.json")

    if request.method == 'POST':
        # print("request.method == 'POST'")
        if flag_update:  # "等待异步task make_new_merge_df完成"
            sleep_flag = True
            sleep_n = 0
            while sleep_flag:
                print("sleep {}".format(5 * sleep_n))
                for file in os.listdir(os.path.join(MEDIA_ROOT, "json")):
                    if re.match(r'[0-9]+.*\.merge_df.json', file):
                        time2_tmp, _, _ = file.split('.')
                        time2_tmp = int(time2_tmp)
                        # print("time2_tmp: {}".format(time2_tmp))
                        if time2_tmp == time2:
                            time2_json = os.path.join(MEDIA_ROOT, "json", file)
                            sleep_flag = False
                            flag_update = False
                time.sleep(5)
                sleep_n += 1

            merge_df = pd.read_json(time2_json)
            for col_ in ['ClinicalInfo_centrifugation_date', 'ClinicalInfo_send_date', 'ExtractInfo_extract_date',
                         'DNAUsageRecordInfo_usage_date', 'LibraryInfo_LB_date', 'CaptureInfo_hybrid_date',
                         'SequencingInfo_send_date', 'SequencingInfo_start_time', 'SequencingInfo_end_time']:
                merge_df.loc[:, col_] = [datetime.datetime.strptime(date_, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                                         if re.match(r'\d+-\d+-\d+T\d+:\d+:\d+\.\d+Z', date_)
                                         else datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date() for date_ in
                                         merge_df.loc[:, col_]]
        # print(merge_df)
        merge_df_columns = list(merge_df.columns)
        filed_idx = [6, 24, 31, 36, 42, 56, 64, 68, 74, 112]
        model_list = request.POST['modellist'].split(', ')
        # print(">>>>>>>>>>>>>> model_list >>>>>>>>")
        # pprint(model_list)
        links_dict = {}
        res_columns_normal = []
        for m in range(len(models_set2)):
            if models_set2[m] in model_list:
                res_columns_normal = res_columns_normal + merge_df_columns[filed_idx[m]:filed_idx[m + 1]]
                for link in model_links[models_set2[m]]:
                    links_dict[link] = 1
        res_columns_link = []
        for link in special_fields:
            if link in links_dict:
                res_columns_link.append(link)
        res_raw = merge_df[res_columns_link + res_columns_normal]
        # print(">>>>>>>>>>>> res_raw.column >>>>>>>>>>>>")
        # pprint(res_raw.columns)
        res_filtered = res_raw
        # print(">>>>>>>>> request.POST['queryset'] >>>>>")
        # print(request.POST['queryset'])
        if request.POST['queryset']:  # 有过滤条件
            filter_total = ""
            for i in request.POST['queryset'].split('\n'):
                filter_line = pd.Series(data=[True] * len(merge_df))
                for j in i.split(' AND '):
                    not_, m, f, vp, v = j.split('\t')
                    not_ = not_[1:]
                    v = v[:-1]
                    # print(">>>>>>>>>> not_, m, f, vp, v >>>>>>>>")
                    # print("%s, %s, %s, %s, %s" % (not_, m, f, vp, v))
                    filter_condition = condition_filter(res_raw, f, vp, v, not_) if f in special_fields else \
                        condition_filter(res_raw, m + '_' + f, vp, v, not_)
                    # print(">>>>>>>>>> filter_condition >>>>>>>>")
                    # print(filter_condition)
                    filter_line = filter_line & filter_condition
                filter_total = filter_line if filter_total == "" else filter_total | filter_line
            res_filtered = res_raw[filter_total]
        # make res_pro
        # print(">>>>>>>>>>>>>> res_filtered >>>>>>>>")
        # pprint(res_filtered)
        link_n = 0
        res_pro_df = pd.DataFrame()
        for link in special_fields:
            if link in links_dict:
                res_pro_df.loc[:, "link%s" % link_n] = list(res_filtered[link])
                link_n = link_n + 1
        normal_n = 0
        for col in res_columns_normal:
            res_pro_df.loc[:, "normal%s" % normal_n] = list(res_filtered[col])
            normal_n = normal_n + 1
        res_pro = res_pro_df.to_dict('records')
        # print('>>>>>>>>>>>>>> res_pro >>>>>>>>')
        # print(res_pro)
        result = {
            'draw': 1,
            'recordsTotal': len(res_raw),
            'recordsFiltered': len(res_pro),
            'data': res_pro
        }
        # print(">>>>>>>>>>>>>> result >>>>>>>>")
        # pprint(result)
        return JsonResponse(result)
    else:
        # print("request.method == 'get'")
        return render(request, 'ADVANCE/AdvancedSearch.html')


def Download_excel(request, model):
    # print(model)
    if model == 'BIS_SampleInventoryInfo':
        file_name = "BIS_SampleInventoryInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'BIS_SampleInfo':
        file_name = "BIS_SampleInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'BIS_ExtractInfo':
        file_name = "BIS_ExtractInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'BIS_DNAUsageRecordInfo':
        file_name = "BIS_DNAUsageRecordInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'LIMS_MethyLibraryInfo':
        file_name = "LIMS_MethyLibraryInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'LIMS_MethyCaptureInfo':
        file_name = "LIMS_MethyCaptureInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'LIMS_MethyPoolingInfo':
        file_name = "LIMS_MethyPoolingInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'SEQ_SequencingInfo':
        file_name = "SEQ_SequencingInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'SEQ_MethyQCInfo':
        file_name = "SEQ_MethyQCInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'LIMS_MethyCaptureInfoPlus':
        file_name = "LIMS_MethyCaptureInfoPlus.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'EMR_ClinicalInfo':
        file_name = "EMR_ClinicalInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'EMR_FollowupInfo':
        file_name = "EMR_FollowupInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'EMR_LiverPathologicalInfo':
        file_name = "EMR_LiverPathologicalInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'EMR_LiverTMDInfo':
        file_name = "EMR_LiverTMDInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif model == 'EMR_LiverBiochemInfo':
        file_name = "EMR_LiverBiochemInfo.template.xlsx"
        file_path = os.path.join(BASE_DIR, "excelData", file_name)
        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response


def plotDataV(request):
    data = {}
    data_sum = 0
    try:
        key1 = KEY1_TO_MODEL[request.GET['model']]
        key2 = request.GET['field']
        values = key1.objects.values_list(key2)
        data_sum = len(values)
        for v in values:
            if isinstance(v[0], str):
                data[v[0]] = data[v[0]] + 1 if v[0] in data else 1
            elif isinstance(v[0], int) or isinstance(v[0], float):
                k = v[0] // 10
                data[k] = data[k] + 1 if k in data else 1
            elif isinstance(v[0], datetime.date):
                k = int("{}01".format(v[0].year)) if v[0].month < 7 else int("{}02".format(v[0].year))
                data[k] = data[k] + 1 if k in data else 1

        for k in data:
            data[k] = round(100 * data[k] / data_sum, 2)
    except FieldError:
        data['空'] = 100

    data_sort = {}
    if isinstance(list(data.keys())[0], str):
        for k in sorted(data, key=lambda x: x):
            data_sort[k] = data[k]
    elif isinstance(list(data.keys())[0], int) or isinstance(list(data.keys())[0], float):
        if re.match(r'^\d{6}$', str(list(data.keys())[0])):
            for k in sorted(data, key=lambda x: x):
                k_str = "{}年上半年".format(str(k)[:4]) if str(k)[4:] == '01' else "{}年下半年".format(str(k)[:4])
                data_sort[k_str] = data[k]
        else:
            for k in sorted(data, key=lambda x: x):
                k_str = "{}~{}".format(int(10 * k), int(10 * (k + 1)))
                data_sort[k_str] = data[k]

    return JsonResponse({'sum': data_sum, 'data': data_sort})
